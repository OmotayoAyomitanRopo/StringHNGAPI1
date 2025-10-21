# test_string_manager.py

from database import create_string, get_string_by_value, delete_string, get_all_strings, DB

def reset_db():
    DB.clear()

def test_create_string():
    reset_db()
    result = create_string("Hello, World!")
    assert result is not None, "Failed to create string."
    assert result['value'] == "Hello, World!", "Stored value does not match."

def test_duplicate_string():
    reset_db()
    create_string("Hello, World!")
    result = create_string("Hello, World!")  # Attempting to add a duplicate
    assert result is None, "Duplicate string should return None."

def test_get_string_by_value():
    reset_db()
    create_string("Test String")
    result = get_string_by_value("Test String")
    assert result is not None, "Failed to retrieve string."
    assert result['value'] == "Test String", "Retrieved value does not match."

def test_delete_string():
    reset_db()
    create_string("Delete Me")
    result = delete_string("Delete Me")
    assert result is not None, "Failed to delete string."
    assert result['value'] == "Delete Me", "Deleted value does not match."
    assert delete_string("Delete Me") is None, "Should return None for already deleted string."

def test_get_all_strings():
    reset_db()
    create_string("String One")
    create_string("String Two")
    all_strings = get_all_strings()
    assert len(all_strings) == 2, "Should return all stored strings."

if __name__ == "__main__":
    test_create_string()
    test_duplicate_string()
    test_get_string_by_value()
    test_delete_string()
    test_get_all_strings()
    
    print("All tests passed!")