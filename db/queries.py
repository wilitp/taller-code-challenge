

def create_project(database, name, description):
    query = """
    INSERT INTO Project (name, description) VALUES (:name, :description) RETURNING id
    """
    return database.execute(query, {"name": name, "description": description})