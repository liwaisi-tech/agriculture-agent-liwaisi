from .current_readings import GetCurrentReadingsTool
from .historical_data import GetHistoricalDataTool
from .analyze_climate import AnalyzeClimateTool
from .crop_info import GetCropInfoTool
from .seasonal_recommendations import GetSeasonalRecommendationsTool
from .general_agriculture_info import GetGeneralAgricultureInfoTool

AVAILABLE_TOOLS = [
    GetCurrentReadingsTool(),
    GetHistoricalDataTool(),
    AnalyzeClimateTool(),
    GetCropInfoTool(),
    GetSeasonalRecommendationsTool(),
    GetGeneralAgricultureInfoTool()
] 