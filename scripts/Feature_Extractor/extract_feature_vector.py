#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parser to extract decent feature strings from shared objects."""

__license__ = "GPL"
__version__ = "2.0"

import angr
import sys, getopt
import json
import magic
import os
import string

def splitn(seq, n):
    printset = set(string.printable)
    group = bytearray()
    nrignored = 0
    for elem in seq:
        if elem != n:
            group.append(elem)
        elif group:
            try:
                mystr = group.decode('utf-8')
                if len(mystr) > 3 and set(mystr).issubset(printset):
                    yield mystr
            except:
                try:
                    mystr = group.decode('ascii')
                    if set(mystr).issubset(printset):
                        yield mystr
                except:
                    nrignored = nrignored+1
            group = bytearray()


def analyzeStrings(target, proj):
    allstrings = []
    likelycommands = []
    debugstrings = []

    # All the funky strings we're currently interested in
    #searchstrings = {'copyright', 'llvm', 'gcc', 'version', 'java'}
    searchstrings = {'version', 'java_package_name'}

    # Grab the section from the shared library
    sharedlib = proj.loader.all_elf_objects.pop()
    rodata = sharedlib.reader.get_section_by_name('.rodata')

    # chunkanize and try to find strings
    allstrings = list(splitn(rodata.data(), 0))

    # Ugly heuristic to identify likely identifiers/commands and debug strings
    for elem in allstrings:
        # Identify identifiers
        if len(elem) > 2 and (elem.isidentifier() or
            (elem.find('::')!=-1 and elem[0:elem.find('::')].isidentifier()
            and elem[elem.find('::')+2:].isidentifier())):
            likelycommands.append(elem)
        # Identify debug strings (according to searchstrings set above)
        elelo = elem.lower()
        for ele in searchstrings:
            if elelo.find(ele) != -1 and len(elem) < 128:
                debugstrings.append(elem)

    # Try to grab the comment section and tokanize it
    try:
        comment = sharedlib.reader.get_section_by_name('.comment')
        commentstrings = list(splitn(comment.data(), 0))
    except:
        commentstrings = []
    for cmt in commentstrings:
        debugstrings.append(cmt)

    return (allstrings, likelycommands, debugstrings)


prunelist = {
   # note: make sure each set contains more than a single entry,
   # otherwise the string is considered a set broken into individual chars
   'fstart': ( 'std::allocator', 'std::vector', 'non-virtual thunk for ', '__aeabi', '_ZNK10__cxxabiv120', '_ZNSt6vector', '__float', '__gnu_Unwind_ForcedUnwind', '__cxa_' ),
                  # risky: this excludes a lot!
   'fcontain' : ( '__gnu_cxx17__normal_iterator', 'xxxxxxxxxxxxxxxxxxxxxxx' ),
   'vstart' : ( 'typeinfo name for ', 'typeinfo for ', 'vtable for ', '__end__', '__bss_start', '__bss_end__', '__bss_start__', '_end', '_edata', '_bss_end__' )
}

prunelistfunc = ( 'std::allocator', 'std::vector', 'non-virtual thunk for ', '__aeabi', '_ZNK10__cxxabiv120' )
prunelistvar = ( 'typeinfo name for ', 'typeinfo for ', 'vtable for ', '__end__', '__bss_start', '__bss_end__', '__bss_start__', '_end', '_edata', '_bss_end__' )


def analyze(target):
    vec = {
            'globalvars': [],
            'importedglobals': [],
            'importedfunctions': [],
            'exportedfunctions': [],
            'allstrings': [],
            'stringidentifiers': [],
            'debugstrings': [],
            'localsymbols': [],
            'dependencies': [],
            'elfname': target[target.rfind('/')+1:]
            }
    if os.path.getsize(target) == 0:
        print('ERROR: Empty file.')
        print('ERROR: Bailing.')
        return vec
        mime = str(magic.from_file(target, mime=True))
    if mime != 'application/x-sharedlib':
        print('ERROR: Expected a ELF shared library but got a:', mime)
        print('ERROR: Bailing.')
        return vec
    try:
        proj = angr.Project(target, auto_load_libs=False)
    except:
        print('ERROR: Angr threw an exception: ',sys.exc_info()[0])
        print('ERROR: Bailing.')
        return vec

    # Parse first batch of information from ELF symbol table
    # Goal: split information based on symbol details
    defined_functions = set()
    imported_functions = set()
    defined_globals = set()
    imported_globals = set()
    local_symbols = set()
    for symb in proj.loader.symbols:
        # ignoring weak symbols for now
        if symb.is_weak:
            continue

        # check functions and variables
        if symb.is_function:
            if symb.is_extern:
                imported_functions.add(symb.name)
            elif symb.is_export:
                defined_functions.add(symb.name)
        else:
            if symb.is_extern:
                imported_globals.add(symb.name)
            elif symb.is_export:
                defined_globals.add(symb.name)

        # cluster any remaining local symbols
        if symb.is_local and not symb.is_export:
            local_symbols.add(symb.name)

    defined_globals = [x for x in defined_globals if not x.startswith(prunelist['vstart'])]
    imported_globals = [x for x in imported_globals if not x.startswith(prunelist['vstart'])]
    local_symbols = [x for x in local_symbols if not x.startswith(prunelist['vstart'])]
    imported_functions = list(filter(lambda x: not x.startswith(prunelist['fstart']) and not any(y in x for y in prunelist['fcontain']), imported_functions))
    defined_functions = list(filter(lambda x: not x.startswith(prunelist['fstart']) and not any(y in x for y in prunelist['fcontain']), defined_functions))

    print(prunelist['fstart'])
    print(prunelist['fcontain'])

    # Go deep into .rodata and extract strings
    (allstrings, likelyfuncs, debugstrings) = analyzeStrings(target, proj)

    # Sum up information and return
    vec['globalvars'] = defined_globals
    vec['importedglobals'] = imported_globals
    vec['importedfunctions'] = imported_functions
    vec['exportedfunctions'] = defined_functions
    vec['localsymbols'] = local_symbols
    vec['dependencies'] = list(proj.loader.requested_names)
    vec['allstrings'] = allstrings
    vec['stringidentifiers'] = likelyfuncs
    vec['debugstrings'] = debugstrings
    vec['elfname'] = list(proj.loader.shared_objects)[0]
    return vec

if __name__ == "__main__":
    infile = ''
    outfile =''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['libfile=', 'jsonfile='])
    except getopt.GetOptError:
        print('Usage: ', sys.argv[0], ' -i <lib.so> -o <out.json>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ', sys.argv[0], ' -i <lib.so> -o <out.json>')
            sys.exit()
        elif opt in ('-i', '--libfile'):
            infile = arg
        elif opt in ('-o', '--jsonfile'):
            outfile = arg
    if infile == '':
        print('Usage: ', sys.argv[0], ' -i <lib.so> -o <out.json>')
        print('Please specify infile!')
        sys.exit()

    vec = analyze(infile)

    if outfile == '':
        print(vec)
    else:
        with open(outfile, 'w') as f:
            json.dump(vec, f)
