from statistique_dao import StatistiquesDAO
from db_connection import DBConnection

StatistiquesDAO(DBConnection()).delete_statistique(id_statistique=0)
