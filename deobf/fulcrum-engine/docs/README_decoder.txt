Fulcrum-specific offline decoder (experimental)

Requirements: Python 3.8 or later. No external packages.

python fulcrum_deobf.py scan path/to/file.lua --direct -o report.json
python fulcrum_deobf.py decrypt O --data '[235,133]' --key '[1,2,3,4,5]' --seed 123
python test_fulcrum.py

The scan detects the Fulcrum header. For the exact previously analyzed
km_e184_ls_1ee.txt loader, it also reports heuristic, previously recovered
string candidates, keyed by source character offsets. Those candidates are
not validated substitutions and should not be treated as verified source.
The optional --direct mode tries to recover simple nearby direct assignments
for decryptor arguments. It is a heuristic: flattened control flow can make
its output wrong. On the known loader it recovered 52 candidates, 32 agreeing
with the earlier, itself unverified, candidate catalog. No source is rewritten.
The decrypt command implements four Fulcrum string transforms using explicit
arguments. It never executes the input, performs network requests, or transmits
keys. It does not reliably recover all string arguments, flatten the VM,
remove authentication, or devirtualize arbitrary Fulcrum scripts. It cannot
produce a complete readable script; this is a working partial decoder, not the
full engine requested. Luraph is separate and is not included.
