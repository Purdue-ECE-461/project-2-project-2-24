from openapi_server.database.tables import users
from openapi_server.database import utils
def new_token_query(auth_request):
        user_id = users.get_user_id(auth_request.user.name)
        new_token_id = utils.gen_new_integer_id("tokens")
        new_token = db_hash(str(round(time.time() * 1000)))
        new_token_hash = db_hash(new_token)

        query = f"""
            INSERT INTO {os.environ["GOOGLE_CLOUD_PROJECT"]}.{self.dataset.dataset_id}.tokens (id, hash_token, created, interactions, user_id)
            VALUES ({new_token_id}, "{new_token_hash}", CURRENT_TIMESTAMP(), {MAX_TOKEN_USES}, {user_id})
        """