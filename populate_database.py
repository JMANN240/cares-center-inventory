from populate_donors import populate_donors
from populate_items import populate_items
from populate_managers import populate_managers
from populate_transactions import populate_transactions
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

populate_donors()
populate_items()
populate_managers()
populate_transactions()