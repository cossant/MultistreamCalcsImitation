from assets.UnitType import UnitType

# TEST VALUES
SUPPOSED_INT_SIZE = 4 # in byts
WORK_DURATION_IN_TICKS_FORK = {
    UnitType.VPU    : (4, 6),
    UnitType.ME     : (5, 5),
    UnitType.FE     : (1, 3)
}
WORK_MAX_BATCH_SIZE = {
    UnitType.VPU    : int(32 / SUPPOSED_INT_SIZE),
    UnitType.ME     : int(32 * 32 / (SUPPOSED_INT_SIZE * SUPPOSED_INT_SIZE)),
    UnitType.FE     : int(32 / SUPPOSED_INT_SIZE)
}
DATA_TRANSACTION_MAX_SIZE = int(1024 / 8 / SUPPOSED_INT_SIZE)          # Bits to bytes to ints conversion
TOTAL_TPC_MEMORY = int(1 * 256 / SUPPOSED_INT_SIZE)       # Gb to ints conversion
TOTAL_HBM_MEMORY = 6 * TOTAL_TPC_MEMORY





## REAL VALUES
# SUPPOSED_INT_SIZE = 4 # in byts
#
# WORK_DURATION_IN_TICKS_FORK = {
#     UnitType.VPU    : (4, 11),
#     UnitType.ME     : (256, 256),
#     UnitType.FE     : (1, 3)
# }
#
# WORK_MAX_BATCH_SIZE = {
#     UnitType.VPU    : int(256 / SUPPOSED_INT_SIZE),
#     UnitType.ME     : int(256 * 256 / (SUPPOSED_INT_SIZE * SUPPOSED_INT_SIZE)),
#     UnitType.FE     : int(4 / SUPPOSED_INT_SIZE)
# }
#
# DATA_TRANSACTION_MAX_SIZE = int(1024 / 8 / SUPPOSED_INT_SIZE)          # Bits to bytes to ints conversion
# TOTAL_TPC_MEMORY = int(1 * 1024 * 1024 * 1024 / SUPPOSED_INT_SIZE)       # Gb to ints conversion
# TOTAL_HBM_MEMORY = 12 * TOTAL_TPC_MEMORY
#
# ????
# Доступ в свою память на TPC = 100.
# Доступ к HBM = [500, 600].