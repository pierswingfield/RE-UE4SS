"""Apply the Galactic Racer FindProperty patch to the upstream e3ba101 UE4SS.dll.

Input:  UE4SS.dll from zDEV-UE4SS_v3.0.1-1152-ge3ba1016.zip (upstream experimental release)
Output: the UE4SS.dll shipped in Galactic Racer Edition Open Beta v0.9.4

The patch is one byte in Unreal::UStruct::FindProperty (UEPseudo). On a name match the
function normally stores the result in its static (UStruct*, FName) -> FProperty* cache
before returning. The patch retargets that `je` to the plain `return rdi` path, so the
cache is never populated and every lookup walks the property chain.

  VA 0x18040048F  je +0x1F3 (0F 84 8E 00 00 00) -> je +0x20E (0F 84 A9 00 00 00)

Usage: python3 patch_findproperty_cache.py <upstream UE4SS.dll> <output UE4SS.dll>
"""
import hashlib
import sys

UPSTREAM_SHA256 = "680a026890abb4d0df2211251f8defc1681a584275f1521dcc0fe30af480006f"
PATCHED_SHA256 = "243b5228ac80a65eefd2eea1a9b9082c4ece676582419448f29886e3c1cd98d9"
FILE_OFFSET = 0x3FF891
OLD_BYTE = 0x8E
NEW_BYTE = 0xA9


def main(src, dst):
    data = bytearray(open(src, "rb").read())
    if hashlib.sha256(data).hexdigest() != UPSTREAM_SHA256:
        sys.exit("input is not the upstream e3ba101 UE4SS.dll")
    if data[FILE_OFFSET] != OLD_BYTE:
        sys.exit(f"unexpected byte at {FILE_OFFSET:#x}")
    data[FILE_OFFSET] = NEW_BYTE
    if hashlib.sha256(data).hexdigest() != PATCHED_SHA256:
        sys.exit("patched output does not match the shipped Galactic Racer DLL")
    open(dst, "wb").write(data)
    print(f"wrote {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
