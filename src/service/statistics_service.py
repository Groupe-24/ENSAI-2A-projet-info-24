class StatisticsService:
    def __init__(self, statistiques_dao):
        self.statistiques_dao = statistiques_dao

    def get_stats_by_player(self, player_id: int):
        stats = self.statistiques_dao.get_statistique_by_id(player_id)
        if stats:
            return {
                "player_id": stats["Joueur"],
                "goals": stats["But"],
                "match_score": stats["Score_De_Match"],
                "boost_usage": stats["Consommation_Du_Boost"],
            }
        return None

    def get_total_goals_by_player(self, player_id: int):
        stats = self.statistiques_dao.list_statistiques()
        total_goals = sum(stat["But"] for stat in stats if stat["Joueur"] == player_id)
        return {"player_id": player_id, "total_goals": total_goals}

    def get_top_performers(self, limit: int = 5, sort_by: str = "goals"):
        stats = self.statistiques_dao.list_statistiques()
        if sort_by == "goals":
            sorted_stats = sorted(stats, key=lambda s: s["But"], reverse=True)
        elif sort_by == "score":
            sorted_stats = sorted(stats, key=lambda s: s["Score_De_Match"], reverse=True)
        else:
            return []

        top_performers = sorted_stats[:limit]
        return [{"player_id": stat["Joueur"], sort_by: stat[sort_by]} for stat in top_performers]
