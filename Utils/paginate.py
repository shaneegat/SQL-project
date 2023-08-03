def paginate_data(page, data):
    items_per_page = 10
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(data))
    current_page_data = data[start_idx:end_idx]
    total_pages = (len(data) + items_per_page - 1) // items_per_page
    return current_page_data, total_pages, page
