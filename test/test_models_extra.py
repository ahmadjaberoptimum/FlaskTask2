from test.helpers import make_user, make_library, make_book

def test_models_to_dict_coverage(app):
    with app.app_context():
        u = make_user("M", "m@test.com")
        lib = make_library(u.id, "MyLib")
        b = make_book(lib.id, "T", "A")

        assert "id" in u.to_dict()
        assert "id" in lib.to_dict()
        assert "id" in b.to_dict()
