import sys
import os

print("Python path:")
for path in sys.path:
    print(path)

print("\nCurrent working directory:")
print(os.getcwd())

try:
    import medhaai
    print("\nmedhaai package found at:")
    print(medhaai.__file__)
except ImportError as e:
    print(f"\nFailed to import medhaai: {e}")