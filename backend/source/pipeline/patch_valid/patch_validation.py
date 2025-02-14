import os
import difflib
import shutil
from typing import Optional

class PatchValidation:
    def __init__(self, patch_dir: str = "patch_candidates", reference_file: str = "fixed_code.java") -> None:
        self.patch_dir = patch_dir
        self.reference_file = reference_file

    def validate_patches(self) -> Optional[str]:
        if not os.path.exists(self.reference_file):
            print(f"Reference file '{self.reference_file}' does not exist.")
            return None

        patch_files = [f for f in os.listdir(self.patch_dir) if f.endswith(".java")]
        if not patch_files:
            print("No patch candidates found.")
            return None

        print(f"Found {len(patch_files)} patch candidates. Validating patches...")

        with open(self.reference_file, "r") as ref_file:
            reference_code = ref_file.read()

        best_patch = None
        best_similarity = 0.0

        for patch_file in patch_files:
            patch_path = os.path.join(self.patch_dir, patch_file)

            with open(patch_path, "r") as patch:
                patch_code = patch.read()

            # Compute similarity ratio
            sm = difflib.SequenceMatcher(None, reference_code, patch_code)
            similarity = sm.ratio()

            print(f"Patch {patch_file} similarity: {similarity:.4f}")

            if similarity > best_similarity:
                best_similarity = similarity
                best_patch = patch_file

        if best_patch:
            print(f"Best patch is {best_patch} with similarity {best_similarity:.4f}")
            shutil.copy(os.path.join(self.patch_dir, best_patch), "best_patch.java")
            return best_patch
        else:
            print("No valid patch found.")
            return None
