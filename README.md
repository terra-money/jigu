# Jigu - The Python SDK for Terra

Jigu (지구, or **Earth** in Korean) is the official Python SDK (Software Development Kit) for Terra, which allows developers to write software that integrates with the Terra blockchain and its ecosystem. You can find the official documentation at our SDK [docs site](https://jigu.terra.money).

## Getting Started

#### Install Jigu

Jigu requires **Python 3.7+**. Install the latest version of Jigu with `pip` on PyPI:

```bash
$ pip install -U jigu
```

#### Connect to Soju testnet

Once you've installed Jigu, fire up an interactive Python shell and connect to the Soju testnet using the official Soju node provided by Terraform Labs.

```python
from jigu import Terra
from jigu.key.mnemonic import MnemonicKey

soju = Terra("soju-0013", "https://soju-lcd.terra.dev")
assert soju.is_connected()
```

#### Create an account

Before we can make any transactions, we have to have an account. Enter in the above to create an account and print its account address.

```python
from jigu.key.mnemonic import MnemonicKey

wallet = soju.wallet(MnemonicKey.generate())
wallet.address
# terra17w4ppj92dwdf93jjtply08nav2ldzw3z2l3wzl
```

#### Top off with testnet funds

Great, now that we have an address, let's get some testnet funds. Head over to the [Soju Faucet](https://soju-faucet.terra.money/) and top off some Luna.

![faucet](./img/faucet.png#shadow)

After that's done, you should have 10,000 LUNA in your account. To confirm this, you can enter the following:

```python
wallet.balance("uluna")
# Coin('uluna', 10000000000)
```

#### Create a transaction

Let's send 23 Testnet Luna to your friend at the following address:

`terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv`

We'll need to create a transaction containing a `MsgSend` alongside a short memo (note) "Hello Jigu!" -- our version of Hello World.

```python
from jigu.core import Coin
from jigu.core.msg import MsgSend

send = MsgSend(
    from_address=wallet.address,
    to_address="terra1wg2mlrxdmnnkkykgqg4znky86nyrtc45q336yv",
    amount=[Coin("uluna", 23_000_000)]
)

tx = wallet.create_and_sign_tx(send, memo="Hello Jigu!")
res = soju.broadcast_tx(tx)
```

#### See it on the blockchain

It should take around 6 seconds to finalize. If everything went well, you should get a result object with the height and TX hash after about 6 seconds.

```python
print(f"TX Hash: {res.txhash}")
# TX Hash: 82D5440A4C4CAB5B74EE3C98CE7F755372CD92E945425A572654179A4A0EE678
```

Copy the TX hash and enter it on [Finder](https://finder.terra.money/), selecting the chain `soju-0013`.

![txhash](./img/txhash.png#shadow)

### A Taste of DeFi

Now that we've gotten our bearings a little, let's take things a bit further and get a glimpse of DeFi (Decentralized Finance) through Terra using Jigu. In this example, we'll be using the Market module to swap stablecoins tracking fiat different fiat currencies.

#### Swap our LUNA for stablecoins

Let's create 1 transaction including 2 `MsgSwap` messages. Terra transactions can include more than one as long as sufficient fee is provided to be accepted. If we do not provide a fee, Jigu will automatically try to estimate a fee before broadcasting. However, the fee estimation mechanism is not always accurate, so here we'll apply a manual one to be safe.

```python
from jigu.core import StdFee
from jigu.core.msg import MsgSwap

swap1 = MsgSwap(
    trader=wallet.address,
    offer_coin=Coin("uluna", 1500_000_000),
    ask_denom="uusd"
)

swap2 = MsgSwap(
    trader=wallet.address,
    offer_coin=Coin("uluna", 2000_000_000),
    ask_denom="ukrw"
)

# Set our gas limit to 250,000 and pay 1 LUNA
fee = StdFee.make(gas=250_000, uluna=1_000_000)
tx = wallet.create_and_sign_tx([swap1, swap2], fee=fee)
res = soju.broadcast_tx(tx)
```

#### See it on the blockchain

```python
print(f"TX Hash: {res.txhash}")
# TX Hash: 04FD23C9A03A6A70118CC6FA6E729F0C442BF44838C7EBCFD7A1B6C4A70168B5
```

![swaptxhash](./img/swaptxhash.png#shadow)

#### Check new account balance

We've successfully swapped our LUNA for stablecoins!

```python
wallet.balance()
# Coins(ukrw=513520000000, uluna=6472992326, uusd=326113463)
```

![account_balances](./img/account_balances.png#shadow)

#### Conclusion

Congratulations! You've successfully gotten set up and are ready to build applications that leverage the robust DeFi infrastructure provided by the Terra network. Explore the rest of Jigu SDK and discover what other awesome things you can build.

## License

This software is licensed under the MIT license. See [LICENSE](./LICENSE.md) for full disclosure.

© 2020 Terraform Labs, PTE.
