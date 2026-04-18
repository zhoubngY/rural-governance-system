from app.crud.base import CRUDBase
from app.models.policy import Policy
from app.schemas.policy import PolicyCreate, PolicyUpdate

class CRUDPolicy(CRUDBase[Policy, PolicyCreate, PolicyUpdate]):
    pass

policy_crud = CRUDPolicy(Policy)