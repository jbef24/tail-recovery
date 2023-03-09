import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Pytest')
import pandas as pd
import numpy as np
from create_datasets.create_grids import add_returns
from create_datasets.constants import RETURNS_FOR_STATISTICS

def test_add_returns():
    logging.info(f'test')

    prices = pd.read_csv(os.path.expanduser('tests/sample_data/aapl_price.csv'))

    prices.index = prices.time
    G = prices.copy()
    prices = prices.drop(columns=['time', 'ticker'])
    from_returns = add_returns(G, prices)

    # Check correct NaN values

    #first one
    assert from_returns['return_t=0'].isnull().sum() == 1
    #last one
    assert from_returns['return_t=1'].isnull().sum() == 1
    #last N
    assert from_returns['return_t=2'].isnull().sum() == 2
    assert from_returns['return_t=4'].isnull().sum() == 4
    assert from_returns['return_t=5'].isnull().sum() == 5
    assert from_returns['return_t=6'].isnull().sum() == 6
    assert from_returns['return_t=19'].isnull().sum() == 19
    assert from_returns['return_t=20'].isnull().sum() == 20
    assert from_returns['return_t=21'].isnull().sum() == 21
    assert from_returns['return_t=252'].isnull().sum() == 252

    logger.info(f'NaN sizes are correct')

    log_prices = prices.copy()
    log_prices = np.log(prices)
    # Check with unshifted data the prices are same
    for return_day in RETURNS_FOR_STATISTICS:
        column = pd.DataFrame(from_returns[f'return_t={return_day}'])

        double_check = log_prices.diff(return_day)

        # the unshifted must be the same as the shifted re-shifted
        assert (~(double_check.close.dropna() == column.shift(return_day).dropna()[f'return_t={return_day}'])).sum() == 0
        logger.info(f'assertion true for return_day={return_day}')