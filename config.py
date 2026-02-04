from models.trade_entity import InstumentType, TimeFrame

CONFIG = {
    "instruments": {
        InstumentType.STOCKS: ["GAZP", "MOEX", "T", "YDEX", "GMKN"],
        InstumentType.FUTURES: ["MMH5", "RBH6", "TBH6", "GKH6", "LKH6"],
    },
    "timeframes": {
        InstumentType.STOCKS: TimeFrame.DAY,
        InstumentType.FUTURES: TimeFrame.HOUR_2,
    },
    "parallel_limit": 5,
    "storage_path": "data"
}
