from UnitType import UnitType

WORK_DURATION_IN_TICKS_FORK = {
    UnitType.VPU    : (4, 11),
    UnitType.ME     : (256, 256),
    UnitType.FE     : (1, 3)
}

WORK_MAX_BATCH_SIZE_IN_BYTES = {
    UnitType.VPU    : 256,
    UnitType.ME     : 256 * 256,
    UnitType.FE     : 4
}

DATA_TRANSACTION_MAX_SIZE_IN_BYTES = 1024 / 8            # Bits to bites conversion (128)
TOTAL_TPC_MEMORY_IN_BYTES = 1 * 1024 * 1024 * 1024       # Gb to bites conversion

COMPUTING_UNITS_COUNT = 4
COMPUTING_UNIT_COMMAND_BUFFER_SIZE = 20

# ????
# Доступ в свою память на TPC = 100.
# Доступ к HBM = [500, 600].