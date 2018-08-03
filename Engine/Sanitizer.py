def sanitize_filename(file_path):
    file_path = file_path.replace('-', '')
    file_path = file_path.replace('/', '_')
    file_path = file_path.replace('\\', '_')
    file_path = file_path.replace(' ', '_')
    file_path = file_path.replace(',', '')
    file_path = file_path.replace(':', '')
    file_path = file_path.replace(';', '')
    return file_path