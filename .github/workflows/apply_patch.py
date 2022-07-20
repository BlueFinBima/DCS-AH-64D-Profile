import sys
infile = sys.argv[1]
patchfile = sys.argv[2]
outfile = sys.argv[3]

from diff_match_patch import diff_match_patch

fi = open(infile,'r')
text = fi.read()
fi.close()

diff = open(patchfile,'r').read()
patched = open(outfile,'w')

dmp = diff_match_patch()
patches = dmp.patch_fromText(diff)

new_text, _ = dmp.patch_apply(patches, text)
if not new_text:
	log.info("Patch did not apply")
	exit()
print(new_text[0:4096])
patched.write(new_text)