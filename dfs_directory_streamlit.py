import os
import streamlit as st

def dfs_directory(path):
    stack = [path]
    visited = set()
    files_found = []
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if os.path.isdir(current):
            try:
                for entry in os.listdir(current):
                    full_path = os.path.join(current, entry)
                    stack.append(full_path)
            except PermissionError:
                continue
        else:
            files_found.append(current)
    return files_found

def dfs_find_files_with_extension(path, extension):
    stack = [path]
    visited = set()
    matched_files = []
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if os.path.isdir(current):
            try:
                for entry in os.listdir(current):
                    full_path = os.path.join(current, entry)
                    stack.append(full_path)
            except PermissionError:
                continue
        else:
            if current.lower().endswith(extension.lower()):
                matched_files.append(current)
    return matched_files

def dfs_search_recipe(collection, target):
    stack = [(collection, [])]
    while stack:
        current, path = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                stack.append((value, path + [key]))
        elif isinstance(current, list):
            for item in current:
                stack.append((item, path))
        else:
            if str(current).lower() == target.lower():
                return path + [current]
    return None

recipes = {
    "Desserts": {
        "Cakes": ["Chocolate Cake", "Vanilla Cake"],
        "Cookies": ["Chocolate Chip Cookie", "Oatmeal Cookie"]
    },
    "Main Course": {
        "Pasta": ["Spaghetti Bolognese", "Penne Arrabiata"],
        "Rice": ["Fried Rice", "Biryani"]
    },
    "Drinks": ["Lemonade", "Mango Smoothie"]
}

st.title("DFS Directory & Recipe Search Example")

root_dir = st.text_input("Enter directory to search (e.g., C:/Users/Public):", value=os.path.expanduser("~"))

st.header("DFS: List All Files")
if st.button("Search Files (DFS)"):
    if os.path.exists(root_dir):
        with st.spinner("Searching..."):
            files = dfs_directory(root_dir)
        st.success(f"Found {len(files)} files.")
        for f in files[:100]:
            st.write(f)
        if len(files) > 100:
            st.info(f"Showing first 100 files out of {len(files)}.")
    else:
        st.error("Directory does not exist.")

st.header("DFS: Find Files by Extension")
file_ext = st.text_input("Enter file extension to search for (e.g., .txt):", value=".txt")
if st.button("Search Files with Extension (DFS)"):
    if os.path.exists(root_dir):
        with st.spinner(f"Searching for *{file_ext} files using DFS..."):
            files = dfs_find_files_with_extension(root_dir, file_ext)
        st.success(f"Found {len(files)} files with extension '{file_ext}'.")
        for f in files[:100]:
            st.write(f)
        if len(files) > 100:
            st.info(f"Showing first 100 files out of {len(files)}.")
    else:
        st.error("Directory does not exist.")

st.header("DFS: Search for Recipe Name in Collection")
st.write("### Recipe Collection:")
st.json(recipes)
recipe_name = st.text_input("Enter recipe name to search for:")
if st.button("Search Recipe (DFS)"):
    result = dfs_search_recipe(recipes, recipe_name)
    if result:
        st.success(f"Recipe found! Path: {' > '.join(result)}")
    else:
        st.warning("Recipe not found.")
