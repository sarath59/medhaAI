import sys
print("Python path:")
for path in sys.path:
    print(path)

print("\nAttempting to import medhaai...")
try:
    import medhaai
    print("medhaai imported successfully")
    print(f"medhaai location: {medhaai.__file__}")
except ImportError as e:
    print(f"Failed to import medhaai: {e}")