# Permissions & Groups Setup

## Custom Permissions on Book Model

The `Book` model in the `bookshelf` app includes the following custom permissions:

- `can_view` – Allows users to view book entries.
- `can_create` – Allows users to create new book entries.
- `can_edit` – Allows users to edit existing book entries.
- `can_delete` – Allows users to delete book entries.

These permissions were defined inside the `Meta` class of the `Book` model.

---

## Groups Configuration

Three user groups have been set up via the Django admin interface:

- **Admins**
  - Permissions: All (`can_view`, `can_create`, `can_edit`, `can_delete`)

- **Editors**
  - Permissions: `can_create`, `can_edit`

- **Viewers**
  - Permissions: `can_view`

Users can be assigned to these groups using the Django admin panel.

---

## Permission Usage in Views

All views that interact with books are protected using Django’s `@permission_required` decorator.

### Example:

```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
