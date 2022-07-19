import sys
infile = sys.argv[1]
patchfile = sys.argv[2]
outfile = sys.argv[3]

from diff_match_patch import diff_match_patch

text = open(infile).read()
diff = open(patchfile).read()
patched = open(outfile,'w')

dmp = diff_match_patch()
patches = dmp.patch_fromText(diff)

new_text, _ = dmp.patch_apply(patches, text)
if not new_text:
	log.info("Patch did not apply")
	exit()
# new_text = new_text.replace("Monitor 1", "Monitor 2")	
print(new_text[0:4096])
patched.write(new_text)