import os
import subprocess
import shutil

class PatchValidation:
    def __init__(self, patch_dir="patch_candidates", test_file="TestSuite.java"):
        self.patch_dir = patch_dir
        self.test_file = test_file

    def validate_patches(self):
        patch_files = [f for f in os.listdir(self.patch_dir) if f.endswith(".java")]
        if not patch_files:
            print("No patch candidates found.")
            return None

        print(f"Found {len(patch_files)} patch candidates. Validating patches...")

        for patch_file in patch_files:
            patch_path = os.path.join(self.patch_dir, patch_file)

            # Create a temporary directory for testing
            temp_dir = "temp_testing"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            # Copy patch file and test suite to the temp directory
            shutil.copy(patch_path, temp_dir)
            shutil.copy(self.test_file, temp_dir)

            # Compile the patch
            compile_result = subprocess.run(
                ["javac", "*.java"],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )

            if compile_result.returncode != 0:
                print(f"Compilation failed for {patch_file}:\n{compile_result.stderr}")
                continue

            # Run the test suite
            test_result = subprocess.run(
                ["java", "-cp", ".", "org.junit.runner.JUnitCore", "TestSuite"],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )

            if "FAILURES!" not in test_result.stdout:
                print(f"Patch {patch_file} passed all tests!")
                shutil.copy(patch_path, "best_patch.java")
                return patch_file

            print(f"Patch {patch_file} failed tests.")

        print("No valid patch found.")
        return None
