from jigu import Terra
from jigu.key.mnemonic import MnemonicKey
from jigu.core import StdFee, Coins
from jigu.core.msg import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract

key = MnemonicKey(
    "measure bargain wheat churn wife divert vacuum west forget eager donor mad pool height feel ship sibling tower boost bright lunar mad village attitude"
)

key2 = MnemonicKey.generate()

terra = Terra("william", "http://localhost:1317")
wallet = terra.wallet(key)

bytecode = ""
with open("contract.wasm", "rb") as contract_file:
    bytecode = contract_file.read().hex()

storecode = MsgStoreCode(wallet.address, bytecode)
storetx = wallet.create_and_sign_tx(
    storecode, fee=StdFee.make(200000000, uluna=1000000)
)
res = wallet.broadcast(storetx)
code_id = res.events.store_code[0].code_id[0]

print(f"Uploaded contract code: {code_id}")

instantiate = MsgInstantiateContract(
    sender=wallet.address,
    code_id=code_id,
    init_msg={
        "decimals": 2,
        "initial_balances": [{"address": wallet.address, "amount": "1000000"}],
        "name": "williamCoin",
        "symbol": "WILL",
    },
    init_coins=Coins(uluna=1000000),
)

instantiatetx = wallet.create_and_sign_tx(
    instantiate, fee=StdFee.make(1000000, uluna=100000)
)
res = wallet.broadcast(instantiatetx)
contract_address = res.events.instantiate_contract[0].contract_address[0]
print(f"Contract uploaded at: {contract_address}")

send = MsgExecuteContract(
    sender=wallet.address,
    contract=contract_address,
    msg={"transfer": {"amount": "5000", "recipient": key2.acc_address}},
    coins=Coins(),
)

sendtx = wallet.create_and_sign_tx(send, fee=StdFee.make(200000, uluna=100000))
res = wallet.broadcast(sendtx)

info = terra.wasm.contract_query(contract_address, {""})

balance1 = terra.wasm.contract_query(
    contract_address, {"balance": {"address": wallet.address}}
)

balance2 = terra.wasm.contract_query(
    contract_address, {"balance": {"address": key2.acc_address}}
)

print(f"{wallet.address} - {balance1}")
print(f"{key2.acc_address} - {balance2}")
