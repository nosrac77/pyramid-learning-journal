# Pyramid Learning Journal

## Step 1

### Views/Routes Used:

* **def list_view(request):
    """Function that generates list of journal entries."""
    with open(os.path.join(STATIC, 'templates/public/index.html')) as f:
        return Response(f.read())**

* **def detail_view(request):
    """Function that generates single journal entry."""
    with open(os.path.join(STATIC, 'data/day-11.html')) as f:
        return Response(f.read())**

* **def create_view(request):
    """Function that generates new view."""
    with open(os.path.join(STATIC, 'templates/public/new_entry.html')) as f:
        return Response(f.read())**

* **def update_view(request):
    """Function that updates existing view."""
    with open(os.path.join(STATIC, 'templates/public/edit_entry.html')) as f:
        return Response(f.read())**

##### Pytest 2.6 & 3.6 Coverage Report - 100%
