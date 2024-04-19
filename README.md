# USTC Auto invitation script

---

## Usage

- 将申请人信息存入inviters.txt中，格式为：
```
    <学号> <密码> <手机号>
```
- 将待入校人信息存入users.txt中，格式为：
```
    <姓名> <手机号> <身份证号>
```
- `python invite.py -i inviters.txt -u users.txt -d 0` 为申请当天进出；
- `python invite.py -i inviters.txt -u users.txt -d 3` 为申请三天后进出；
- `python invite.py -i inviters.txt -u users.txt -d 2025-3-32` 为申请2025年3月32日进出。
