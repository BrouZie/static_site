import os
import shutil
from pathlib import Path


def copy_tree_recursive(src: Path, dst: Path) -> None:
    """
    Recursively copy all files and subdirectories from src into dst.
    Assumes dst already exists as a directory.
    """
    # Base case: nothing to copy
    if not src.exists():
        return

    for entry in src.iterdir():
        target = dst / entry.name
        if entry.is_file():
            # ensure parent exists (paranoia for deeply nested paths)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, target)
            print(f"Copied file: {entry} -> {target}")
        elif entry.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            print(f"Entering directory: {entry}")
            copy_tree_recursive(entry, target)
        else:
            # Optional: handle symlinks or special files; skipping is fine for this assignment.
            print(f"Skipping non-regular file: {entry}")


def main() -> None:
    cwd = Path(os.getcwd())
    static_dir = cwd / "static"
    public_dir = cwd / "public"

    # Safety checks
    if not static_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {static_dir}")

    # Ensure we’re not deleting the source by mistake
    try:
        static_dir.relative_to(public_dir)
        raise RuntimeError("Refusing to run: 'static' is inside 'public'.")
    except ValueError:
        pass  # OK: static is not inside public

    try:
        public_dir.relative_to(static_dir)
        raise RuntimeError("Refusing to run: 'public' is inside 'static'.")
    except ValueError:
        pass  # OK: public is not inside static

    # 1) Delete destination (if present) so copy is clean
    if public_dir.exists():
        print(f"Removing existing directory: {public_dir}")
        shutil.rmtree(public_dir)

    # 2) Recreate destination root
    public_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created destination root: {public_dir}")

    # 3) Recursively copy content
    copy_tree_recursive(static_dir, public_dir)
    print("Done.")


if __name__ == "__main__":
    main()
