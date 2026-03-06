from UnitType import UnitType

SUPPOSED_INT_SIZE = 4 # in byts

WORK_DURATION_IN_TICKS_FORK = {
    UnitType.VPU    : (4, 11),
    UnitType.ME     : (256, 256),
    UnitType.FE     : (1, 3)
}

WORK_MAX_BATCH_SIZE = {
    UnitType.VPU    : 256 / SUPPOSED_INT_SIZE,
    UnitType.ME     : 256 * 256 / (SUPPOSED_INT_SIZE * SUPPOSED_INT_SIZE),
    UnitType.FE     : 4 / SUPPOSED_INT_SIZE
}

DATA_TRANSACTION_MAX_SIZE = 1024 / 8 / SUPPOSED_INT_SIZE          # Bits to bytes to ints conversion
TOTAL_TPC_MEMORY = 1 * 1024 * 1024 * 1024 / SUPPOSED_INT_SIZE       # Gb to ints conversion

COMPUTING_UNITS_COUNT = 4
COMPUTING_UNIT_COMMAND_BUFFER_SIZE = 20

# ????
# Доступ в свою память на TPC = 100.
# Доступ к HBM = [500, 600].