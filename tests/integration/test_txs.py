import pytest

from jigu import Terra
from jigu.key.mnemonic import MnemonicKey
from jigu.core.msg import *
from jigu.core import StdFee, Coin
from jigu.error import CodespaceError, TxCodespaceError
from jigu.core.sdk.coin import Coins


class TestTx:
    def test_broadcast(self, wallet, fee):
        swap = MsgSwap(
            trader=wallet.address, offer_coin=Coin("uluna", 1), ask_denom="umnt"
        )
        tx = wallet.create_and_sign_tx(swap, fee=fee)
        res = wallet.broadcast(tx)
        assert res.msgs is not None

    def test_broadcast_txcodespacerror(self, wallet, fee, mnemonics):
        """Tests that a that it captures the correct txcodespace error."""
        fail_swap = MsgSwap(
            trader=wallet.address, offer_coin=Coin("uluna", 1), ask_denom="bebo"
        )
        fail_vote = MsgExchangeRateVote(
            exchange_rate="603.899000000000000000",
            salt="0dff",
            denom="umnt",
            feeder=wallet.address,
            validator="terravaloper1vqnhgc6d0jyggtytzqrnsc40r4zez6tx99382w",
        )
        send = MsgSend(
            from_address=wallet.address,
            to_address=mnemonics[1]["address"],
            amount=Coins(uluna=1),
        )

        tx1 = wallet.create_and_sign_tx(send, send, fail_swap, send, fail_vote, fee=fee)
        with pytest.raises(TxCodespaceError) as excinfo:
            wallet.broadcast(tx1)
        err = excinfo.value
        assert err.codespace == "market"

        tx2 = wallet.create_and_sign_tx(
            send, fail_vote, send, send, fail_swap, fail_swap, fee=fee
        )
        with pytest.raises(TxCodespaceError) as excinfo:
            wallet.broadcast(tx2)
        err = excinfo.value
        assert err.codespace == "oracle"
