## Evaluation Results:##

`Librarian-ICSE2021-RQs.xlsx` under `evaluation-results`
 contains an extended version of the evaluation results presented in the paper (Section 3). Each table’s result is represented in a separate sheet:
* **inferred_libs**: Contains the results of using Librarian to infer the versions of 7251 binaries extracted from android apps. Each binary is represented in one row, with:
  * The name of the cluster/folder which the binary resides in (column A).
  * The name of the binary, represented as *binaryName_* then the *sha256 of the app* which the binary was extracted from (column B).
  * The number of other similar binaries (i.e. binaries that share the same sha256) that reside in the same cluster (column C).
  * The binary's architecture (column D and E).
  * The binary version inferred by Librarian (column F).
  * Whether a binary is vulnerable or not (column G).
* **vul_libs_only**: This table is similar to the previous sheet, but contains vulnerable binaries only 
* **vul_libs_till-now**: Contains the binaries that were vulnerable up until the submission of the paper. Each row contains a vulnerable binary version (column C), along with the name of the distinct app affected by the vulnerable binary (column A), the number of app versions containing a vulnerable binary (column B), and since when was the binary vulnerable (column D). The dates were obtained from [AndroZoo](https://androzoo.uni.lu/lists).
* The remaining sheets are an extended version of the results reported in the paper (table 4 - table 8). Please refer to the paper for more details.   

