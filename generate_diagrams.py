# -*- coding: utf-8 -*-
"""Sinh toàn bộ sơ đồ PNG cho báo cáo ĐATN ShopVolo v2.

Mỗi sơ đồ được vẽ bằng PlantUML (render qua kroki.io) và xuất vào Hinhve/.
Nội dung sơ đồ bám sát mã nguồn thực tế của codebase multi-e-commerce:
  - apps/api-core (NestJS): TenantMiddleware, TenantService, BetterAuthGuard,
    OrderService.createOrder, LayoutService (draft/publish, seed)
  - apps/storefront (Next.js): proxy.ts, dynamic-loader.tsx, storefront.api.ts
  - packages/: ui-registry, schema, database, master-templates, i18n
Quy tắc vẽ theo IT3120: actor người que, tên đối tượng gạch chân, hộp kích
hoạt trên trục thời gian, thông điệp đánh số, trả về nét đứt, khung alt/opt.
"""

import json
import os
import urllib.request

STYLE = """skinparam monochrome true
skinparam shadowing false
skinparam defaultFontSize 13
"""

SEQ_STYLE = STYLE + """skinparam sequenceMessageAlign center
autonumber
"""


def generate(puml, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    url = "https://kroki.io/plantuml/png"
    data = json.dumps({"diagram_source": puml}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response, open(filename, "wb") as out:
            out.write(response.read())
        print(f"OK   {filename}")
    except Exception as e:
        print(f"FAIL {filename}: {e}")


# ============================================================
# CHƯƠNG 2 — USE CASE
# ============================================================

usecase_tong_quat = """@startuml
left to right direction
""" + STYLE + """skinparam packageStyle rectangle
actor "Chủ cửa hàng\\n(Tenant Owner)" as Tenant
actor "Khách hàng\\n(End Customer)" as Customer

rectangle "Hệ thống ShopVolo v2" {
  usecase "UC-01: Khởi tạo cửa hàng" as UC01
  usecase "UC-02: Quản lý khuyến mãi" as UC02
  usecase "UC-03: Tùy biến giao diện\\nvà thương hiệu" as UC03
  usecase "UC-04: Quản lý sản phẩm" as UC04
  usecase "UC-05: Thiết lập menu điều hướng" as UC05
  usecase "UC-06: Tạo trang nội dung động" as UC06
  usecase "UC-10: Ánh xạ tên miền tùy chỉnh" as UC10

  usecase "UC-07: Duyệt sản phẩm\\ntrên trang cửa hàng" as UC07
  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "UC-09: Thanh toán và\\nxử lý đơn hàng" as UC09
}

Tenant -- UC01
Tenant -- UC02
Tenant -- UC03
Tenant -- UC04
Tenant -- UC05
Tenant -- UC06
Tenant -- UC10
Tenant -- UC09

Customer -- UC07
Customer -- UC08
Customer -- UC09
@enduml
"""

usecase_quan_ly_shop = """@startuml
left to right direction
""" + STYLE + """skinparam packageStyle rectangle
actor "Chủ cửa hàng\\n(Tenant Owner)" as Tenant

rectangle "Phân hệ Quản lý cửa hàng" {
  usecase "UC-01: Khởi tạo cửa hàng" as UC01
  usecase "Chọn mẫu giao diện\\ntheo ngành hàng" as UCtpl
  usecase "UC-02: Quản lý khuyến mãi" as UC02
  usecase "UC-03: Tùy biến giao diện\\nvà thương hiệu" as UC03
  usecase "Lưu bản nháp bố cục" as UCdraft
  usecase "Xuất bản giao diện" as UCpub
  usecase "UC-05: Thiết lập menu điều hướng" as UC05
  usecase "UC-10: Ánh xạ tên miền tùy chỉnh" as UC10
  usecase "Xác minh tên miền" as UCverify
}

Tenant -- UC01
Tenant -- UC02
Tenant -- UC03
Tenant -- UC05
Tenant -- UC10

UC01 .> UCtpl : <<include>>
UC03 .> UCdraft : <<include>>
UC03 .> UCpub : <<include>>
UC10 .> UCverify : <<include>>
@enduml
"""

usecase_san_pham_don_hang = """@startuml
left to right direction
""" + STYLE + """skinparam packageStyle rectangle
actor "Chủ cửa hàng\\n(Tenant Owner)" as Tenant
actor "Khách hàng\\n(End Customer)" as Customer

rectangle "Phân hệ Sản phẩm và Đơn hàng" {
  usecase "UC-04: Quản lý sản phẩm" as UC04
  usecase "Thêm và cập nhật\\nsản phẩm" as AddProduct
  usecase "Quản lý biến thể\\nvà giá bán" as PriceProduct
  usecase "Kiểm soát tồn kho" as Inventory
  usecase "Tải lên ảnh sản phẩm" as UploadImg

  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "UC-09: Thanh toán và\\nđặt đơn hàng" as UC09
  usecase "Xử lý đơn hàng\\n(xác nhận, hủy, hoàn tiền)" as ProcessOrder
}

Tenant -- UC04
UC04 .> AddProduct : <<include>>
UC04 .> PriceProduct : <<include>>
UC04 .> Inventory : <<include>>
UC04 .> UploadImg : <<include>>

Customer -- UC08
Customer -- UC09
UC09 .> UC08 : <<include>>
Tenant -- ProcessOrder
@enduml
"""

usecase_khach_hang = """@startuml
left to right direction
""" + STYLE + """skinparam packageStyle rectangle
actor "Khách hàng\\n(End Customer)" as Customer

rectangle "Phân hệ Trải nghiệm khách hàng" {
  usecase "UC-06: Xem trang nội dung" as UC06
  usecase "UC-07: Duyệt sản phẩm\\ntrên trang cửa hàng" as UC07
  usecase "Lọc theo danh mục\\nvà khoảng giá" as Filter
  usecase "Tìm kiếm sản phẩm" as Search
}

Customer -- UC06
Customer -- UC07
Filter .> UC07 : <<extend>>
Search .> UC07 : <<extend>>
@enduml
"""

# ============================================================
# CHƯƠNG 2 — ACTIVITY
# ============================================================

activity_onboarding = """@startuml
""" + STYLE + """
|Chủ cửa hàng|
start
:Đăng ký / đăng nhập tài khoản;
:Điền thông tin cửa hàng,\\nchọn mẫu theo ngành hàng;
|Ứng dụng Admin|
:Gửi POST /api/shops\\n(name, domain, templateKey);
|API Core|
:Tạo bản ghi Shop trong PostgreSQL;
:Xóa cache danh sách shop của chủ sở hữu;
|Ứng dụng Admin|
:Gọi POST /api/layouts/{shopId}/seed;
|API Core|
if (Tài liệu bố cục còn trống?) then (đúng)
  :Gieo bố cục mặc định: GlobalLayout\\n+ 3 trang khởi điểm (MongoDB);
else (đã có nội dung)
  :Bỏ qua, không ghi đè (lũy đẳng);
endif
|Chủ cửa hàng|
:Kéo thả tùy biến giao diện\\n(lưu vào draftData);
:Bấm xuất bản;
|API Core|
:Sao chép draftData sang publishedData;
|Khách hàng|
:Truy cập tên miền cửa hàng;
|Storefront|
:proxy.ts bóc tách định danh cửa hàng,\\nviết lại đường dẫn nội bộ;
:Tải publishedData và dữ liệu sản phẩm;
:Kết xuất giao diện động (RSC);
|Khách hàng|
:Nhận trang web hoàn chỉnh;
stop
@enduml
"""

activity_upload_product = """@startuml
""" + STYLE + """
|Chủ cửa hàng|
start
:Chọn ảnh, gửi multipart\\nPOST /api/media/upload;
|API Core|
if (Kích thước tệp <= 10MB?) then (đúng)
  :Đọc magic bytes,\\nxác định MIME thực của tệp;
  if (Là tệp ảnh hợp lệ?) then (đúng)
    :Trích kích thước ảnh (sharp);
    :Sinh mã BlurHash làm ảnh giữ chỗ;
    |Hạ tầng lưu trữ|
    :Ghi object vào MinIO;
    |API Core|
    :Lưu bản ghi Media (PostgreSQL)\\ngồm URL, kích thước, BlurHash;
    |Chủ cửa hàng|
    :Nhận URL ảnh và BlurHash;
    note right
      Khi hiển thị, imgproxy biến đổi ảnh
      theo chiều rộng và chất lượng yêu cầu
      (resize on-the-fly), không lưu sẵn
      nhiều phiên bản kích thước.
    end note
    stop
  else (sai)
    :Trả lỗi 400:\\nloại tệp không hợp lệ;
    |Chủ cửa hàng|
    :Nhận thông báo lỗi;
    stop
  endif
else (sai)
  :Trả lỗi 400: vượt giới hạn 10MB;
  |Chủ cửa hàng|
  :Nhận thông báo lỗi;
  stop
endif
@enduml
"""

activity_checkout = """@startuml
""" + STYLE + """
|Khách hàng|
start
:Xác nhận giỏ hàng, địa chỉ giao,\\nvận chuyển và phương thức thanh toán;
|Storefront|
:Gửi POST /api/orders/checkout;
|API Core|
if (Request thiếu lineItems?) then (đúng)
  :Đọc giỏ hàng server-side\\ntheo (shopId, customerId);
endif
:Nạp giá các Variant thuộc đúng shopId;
if (Có mã khuyến mãi?) then (có)
  :Kiểm tra hiệu lực, thời hạn\\nvà giới hạn lượt dùng;
endif
:Tính phí vận chuyển, chốt địa chỉ nhận;
:Kiểm tra phương thức thanh toán thuộc cửa hàng;
partition "Giao dịch nguyên tử (PostgreSQL)" {
  :Trừ tồn kho từng Variant;
  :Ghi nhận lượt dùng khuyến mãi;
  if (Thanh toán bằng ví?) then (có)
    :Trừ số dư ví\\n(thiếu thì rollback toàn bộ);
  endif
  :Tạo Order kèm các LineItem;
  :Tạo bản ghi Payment;
  :Xóa giỏ hàng;
  :Tạo Shipment trạng thái pending;
  if (Chuyển khoản ngân hàng?) then (có)
    :Tạo token xác nhận hiệu lực 24 giờ;
  endif
}
if (Chuyển khoản ngân hàng?) then (có)
  :Sinh mã QR từ URL xác nhận\\n(ngoài giao dịch);
endif
:Gửi thông báo WebSocket\\nvà email xác nhận đơn;
|Khách hàng|
:Nhận trang xác nhận đơn hàng;
stop
@enduml
"""

# ============================================================
# CHƯƠNG 4 — KIẾN TRÚC, LỚP, TRÌNH TỰ, ER
# ============================================================

package_diagram = """@startuml
""" + STYLE + """skinparam packageStyle rectangle

package "Tầng ứng dụng (apps)" as LayerApps {
  [admin\\n(Next.js)] as admin
  [storefront\\n(Next.js)] as storefront
  [api-core\\n(NestJS)] as apicore
  [cli-tool\\n(công cụ vận hành)] as cli
}

package "Tầng gói dùng chung (packages)" as LayerPkgs {
  [ui-registry] as uireg
  [i18n] as i18n
  [schema] as schema
  [master-templates] as mtpl
  [database] as db
}

package "Tầng hạ tầng (infrastructure)" as LayerInfra {
  database "PostgreSQL" as pg
  database "MongoDB" as mongo
  database "Redis" as redis
  [MinIO] as minio
  [imgproxy] as imgproxy
}

' Ép xếp ba tầng theo chiều dọc
admin -[hidden]down-> i18n
cli -[hidden]down-> mtpl
i18n -[hidden]down-> redis
schema -[hidden]down-> pg
mtpl -[hidden]down-> mongo

admin ..> uireg
admin ..> i18n
storefront ..> uireg
storefront ..> i18n
storefront ..> schema
uireg ..> schema
apicore ..> db
cli ..> mtpl

admin --> apicore : REST API
storefront --> apicore : REST API
cli --> apicore : REST API
storefront ..> imgproxy : URL ảnh

db ..> pg : Prisma
db ..> mongo : Mongoose
apicore ..> mongo : Mongoose
apicore ..> redis : cache-manager
apicore ..> minio : S3 API
imgproxy ..> minio : đọc ảnh gốc
@enduml
"""

apicore_detail = """@startuml
""" + STYLE + """skinparam packageStyle rectangle
left to right direction

package "api-core (NestJS)" {
  package "Tầng Middleware / Guard" {
    [TenantMiddleware] as tmw
    [BetterAuthGuard] as guard
  }
  package "Tầng Controller" {
    [OrderController] as octrl
    [LayoutController] as lctrl
    [ShopController] as sctrl
  }
  package "Tầng Service" {
    [OrderService] as osvc
    [LayoutService] as lsvc
    [ShopService] as ssvc
    [TenantService\\n(AsyncLocalStorage)] as tsvc
    [AuthService] as asvc
  }
  package "Tầng truy cập dữ liệu" {
    [PrismaService] as prisma
    [Mongoose Models] as mongoose
  }
}

database "Redis" as redis
database "PostgreSQL" as pg
database "MongoDB" as mongo

tmw --> redis : tra cứu domain,\\ntrạng thái shop
tmw --> prisma : truy vấn khi\\ntrượt cache
tmw --> tsvc : run({shopId}, next)
guard --> asvc : kiểm tra phiên
guard --> redis : cache shopIds

tmw --> guard
guard --> octrl
guard --> lctrl
guard --> sctrl

octrl --> osvc
lctrl --> lsvc
sctrl --> ssvc

osvc --> tsvc : getTenantId()
lsvc --> tsvc : getTenantId()
ssvc --> tsvc : getTenantId()

osvc --> prisma
ssvc --> prisma
asvc --> prisma
lsvc --> mongoose

prisma --> pg
mongoose --> mongo
@enduml
"""

class_diagram = """@startuml
""" + STYLE + """skinparam classAttributeIconSize 0
hide circle

class TenantService {
  - {static} als: AsyncLocalStorage<TenantContext>
  + run(context: TenantContext, callback: Function): void
  + getTenantId(): string
}

class TenantMiddleware {
  - tenantService: TenantService
  - prisma: PrismaService
  - cacheManager: Cache
  + use(req: Request, res: Response, next: Function): void
}

class BetterAuthGuard {
  - authService: AuthService
  - reflector: Reflector
  - prisma: PrismaService
  - cacheManager: Cache
  + canActivate(context: ExecutionContext): boolean
}

class AuthService {
  - prisma: PrismaService
  - ownerAuth: OwnerAuth
  - customerAuth: CustomerAuth
  + getOwnerSession(request: Request): Session
  + getCustomerSession(request: Request): Session
  + register(dto): BaseResponseDto
  + login(dto): BaseResponseDto
}

class OrderService {
  - prisma: PrismaService
  - tenantService: TenantService
  - inventoryService: InventoryService
  - emailService: EmailService
  - walletService: WalletService
  + createOrder(customerId: string, dto: CheckoutDto): Order
  + findAllOrders(query: GetOrdersDto): Order[]
  + updateOrderStatus(id: string, dto): Order
  + cancelOrder(id: string, customerId?: string): Order
  + refundOrder(id: string): Order
}

class LayoutService {
  - tenantService: TenantService
  - globalLayoutModel: Model<GlobalLayout>
  - pageLayoutModel: Model<PageLayout>
  + getGlobalLayout(shopId: string): JSON
  + getPageLayout(shopId, pageType, slug?): JSON
  + saveBuilderGlobal(shopId, components, theme): JSON
  + publishLayoutByShopId(shopId: string): JSON
  + seedDefaultLayouts(shopId, opts): JSON
}

class PrismaService {
  + onModuleInit(): void
  + $transaction(fn): Promise<any>
}

TenantMiddleware ..> TenantService : <<use>>
TenantMiddleware ..> PrismaService : <<use>>
BetterAuthGuard ..> AuthService : <<use>>
BetterAuthGuard ..> PrismaService : <<use>>
OrderService ..> TenantService : <<use>>
OrderService ..> PrismaService : <<use>>
LayoutService ..> TenantService : <<use>>
AuthService ..> PrismaService : <<use>>
@enduml
"""

seq_checkout = """@startuml
""" + SEQ_STYLE + """
actor "Khách hàng" as KH
participant "__:OrderController__" as OC
participant "__:OrderService__" as OS
participant "__:InventoryService__" as IS
participant "__:PrismaService__" as PR

KH -> OC : POST /api/orders/checkout (dto)
activate OC
OC -> OS : createOrder(customerId, dto)
activate OS
OS -> PR : variant.findMany({id in dto, shopId})
activate PR
PR --> OS : danh sách Variant kèm giá
deactivate PR

opt dto có promotionCode
  OS -> PR : promotion.findFirst({shopId, code})
  activate PR
  PR --> OS : thông tin khuyến mãi
  deactivate PR
end

OS -> PR : $transaction(fn)
activate PR

alt đủ tồn kho
  PR -> IS : decrementStock(lineItems, orderId, tx)
  activate IS
  IS --> PR : trừ kho thành công
  deactivate IS
  PR -> PR : order.create(kèm lineItems)
  PR -> PR : payment.create()
  PR -> PR : cartItem.deleteMany()
  PR -> PR : shipment.create()
  PR --> OS : Order {id, number, state}
else hết hàng / thiếu số dư ví
  PR --> OS : ném ngoại lệ, rollback toàn bộ
end
deactivate PR

OS ->> OS : gửi thông báo + email (bất đồng bộ)
OS --> OC : finalOrder (kèm QR nếu chuyển khoản)
deactivate OS
OC --> KH : HTTP 201 Created / 400 Bad Request
deactivate OC
@enduml
"""

seq_auth = """@startuml
""" + SEQ_STYLE + """
actor "Người dùng" as ND
participant "__:BetterAuthGuard__" as G
participant "__:AuthService__" as AS
participant "__:better-auth__" as BA
participant "__:PrismaService__" as PR

ND -> G : HTTP Request (cookie phiên)
activate G

alt endpoint gắn @Public()
  G --> ND : cho qua, không kiểm tra
else endpoint cần xác thực
  G -> AS : getOwnerSession(request)\\nhoặc getCustomerSession(request)
  activate AS
  AS -> BA : api.getSession({headers})
  activate BA
  BA --> AS : {user, session} hoặc null
  deactivate BA
  AS --> G : kết quả phiên
  deactivate AS

  alt [phiên hợp lệ]
    G -> PR : shop.findMany({ownerId})\\n(khi trượt cache shopIds)
    activate PR
    PR --> G : danh sách shopId sở hữu
    deactivate PR
    G --> ND : canActivate = true\\n(gắn user, shopIds vào request)
  else [phiên không hợp lệ]
    G --> ND : 401 Unauthorized
  end
end
deactivate G
@enduml
"""

er_diagram = """@startuml
""" + STYLE + """hide circle
skinparam linetype ortho

entity "User" as user {
  * id : uuid <<PK>>
  --
  email
  name
}

entity "Shop" as shop {
  * id : uuid <<PK>>
  --
  * ownerId : uuid <<FK>>
  name
  domain <<unique>>
  status
  currency
}

entity "Customer" as cust {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  email
}

entity "Product" as prod {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  categoryId : uuid <<FK>>
  name
  slug
}

entity "Variant" as vari {
  * id : uuid <<PK>>
  --
  * productId : uuid <<FK>>
  * shopId : uuid <<FK>>
  sku
  price
}

entity "Order" as ord {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  * customerId : uuid <<FK>>
  number <<unique>>
  state
  paymentState
  totalAmount
}

entity "LineItem" as li {
  * id : uuid <<PK>>
  --
  * orderId : uuid <<FK>>
  * variantId : uuid <<FK>>
  quantity
  price
}

entity "Payment" as pay {
  * id : uuid <<PK>>
  --
  * orderId : uuid <<FK>>
  * paymentMethodId : uuid <<FK>>
  amount
  state
}

entity "PaymentMethod" as pm {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  type
}

entity "Cart" as cart {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  * customerId : uuid <<FK>>
}

entity "CartItem" as ci {
  * id : uuid <<PK>>
  --
  * cartId : uuid <<FK>>
  * variantId : uuid <<FK>>
  quantity
}

entity "Shipment" as ship {
  * id : uuid <<PK>>
  --
  * orderId : uuid <<FK>>
  * shopId : uuid <<FK>>
  state
}

entity "Promotion" as promo {
  * id : uuid <<PK>>
  --
  * shopId : uuid <<FK>>
  code
  discountType
  discountValue
}

user ||--o{ shop : sở hữu
shop ||--o{ cust : có
shop ||--o{ prod : có
prod ||--o{ vari : gồm
shop ||--o{ promo : có
shop ||--o{ pm : cấu hình
cust ||--o{ ord : đặt
ord ||--|{ li : gồm
vari ||--o{ li : tham chiếu
ord ||--o{ pay : có
pm ||--o{ pay : qua
cust ||--o{ cart : có
cart ||--o{ ci : gồm
vari ||--o{ ci : tham chiếu
ord ||--o{ ship : giao bởi
@enduml
"""

# ============================================================
# CHƯƠNG 5 — BA ĐÓNG GÓP
# ============================================================

seq_tenant_context = """@startuml
""" + SEQ_STYLE + """
actor "Khách hàng" as KH
participant "__:TenantMiddleware__" as TM
participant "__:Redis__" as RD
participant "__:PrismaService__" as PR
participant "__:TenantService__" as TS
participant "__:OrderController__" as OC
participant "__:OrderService__" as OS

KH -> TM : GET /api/...\\n(Host: duck.myapp.com)
activate TM
TM -> TM : bóc tách subdomain "duck"
TM -> RD : get("domain:duck")
activate RD
RD --> TM : kết quả cache
deactivate RD

alt trúng cache
  TM -> TM : dùng {id, status} từ cache
else trượt cache
  TM -> PR : shop.findUnique({domain: "duck"})
  activate PR
  PR --> TM : {id, status}
  deactivate PR
  TM -> RD : set("domain:duck", shop, 300s)
end

opt status = SUSPENDED
  TM --> KH : HTTP 403 Shop is suspended
end

TM -> TS : run({shopId}, next)
activate TS
TS -> OC : thực thi chuỗi xử lý\\ntrong vùng ngữ cảnh
activate OC
OC -> OS : createOrder(customerId, dto)
activate OS
OS -> TS : getTenantId()
TS --> OS : shopId
OS -> PR : truy vấn ràng buộc theo shopId
activate PR
PR --> OS : dữ liệu đúng phạm vi cửa hàng
deactivate PR
OS --> OC : kết quả nghiệp vụ
deactivate OS
OC --> KH : HTTP Response
deactivate OC
deactivate TS
deactivate TM
@enduml
"""

zero_file_render = """@startuml
""" + STYLE + """
start
:Trình duyệt yêu cầu\\nduck.example.com/;
partition "proxy.ts (Next.js Middleware)" {
  :Bóc tách định danh cửa hàng từ Host;
  :Viết lại đường dẫn nội bộ thành /duck/...\\n(URL trình duyệt không đổi);
}
partition "React Server Components" {
  :Tải song song PageLayout\\nvà thông tin cửa hàng;
  if (Data Cache còn hiệu lực?) then (còn)
    :Dùng JSON bố cục trong cache\\n(tag: layout-{shopId}-page);
  else (hết hạn)
    :GET /api/layouts/{shopId}/page/home\\n(header x-shop-id);
    note right
      api-core chỉ đọc trường publishedData
      bằng truy vấn lean() + projection
    end note
    :Ghi lại Data Cache (revalidate 60s);
  endif
}
partition "DynamicRenderer" {
  while (Còn UIComponentRef trong bố cục?) is (còn)
    :Tra componentId trong ComponentRegistry;
    if (Tìm thấy component?) then (có)
      :Nạp chunk qua next/dynamic\\n(chỉ tải khi bố cục dùng);
      :Kết xuất trong ErrorBoundary,\\nhợp nhất props với pageContext;
    else (không)
      :Hiển thị khung cảnh báo\\n"Missing Component";
    endif
  endwhile (hết)
}
:Truyền HTML hoàn chỉnh về trình duyệt;
stop
@enduml
"""

template_layered_config = """@startuml
""" + STYLE + """skinparam packageStyle rectangle

rectangle "Lược đồ thành phần\\n(giá trị mặc định từng trường)" as schemas
rectangle "Master Template\\n(catalog theo ngành hàng\\n+ gói master-templates)" as master

database "MongoDB" {
  rectangle "GlobalLayout / PageLayout" {
    rectangle "draftData\\n(bản nháp)" as draft
    rectangle "publishedData\\n(bản xuất bản)" as pub
  }
}

rectangle "Trình thiết kế kéo thả\\n(ứng dụng Admin)" as builder
rectangle "Động cơ kết xuất động\\n(ứng dụng Storefront)" as sf

master --> draft : gieo khi khởi tạo\\n(lũy đẳng, chỉ ghi tài liệu trống)
master --> pub : gieo khi khởi tạo
schemas --> builder : sinh form chỉnh sửa,\\nhợp nhất giá trị mặc định
builder --> draft : lưu bản nháp
draft --> builder : đọc nháp (trống thì\\nlấy bản xuất bản)
draft --> pub : xuất bản: sao chép nguyên tử\\n(từng trang hoặc bulkWrite)
pub --> sf : chỉ đọc\\n(lean + projection)
@enduml
"""

# ============================================================

DIAGRAMS = {
    # Chương 2
    "Hinhve/Chuong2/usecase_tong_quat.png": usecase_tong_quat,
    "Hinhve/Chuong2/usecase_quan_ly_shop.png": usecase_quan_ly_shop,
    "Hinhve/Chuong2/usecase_san_pham_don_hang.png": usecase_san_pham_don_hang,
    "Hinhve/Chuong2/usecase_khach_hang.png": usecase_khach_hang,
    "Hinhve/Chuong2/activity_onboarding.png": activity_onboarding,
    "Hinhve/Chuong2/activity_upload_product.png": activity_upload_product,
    "Hinhve/Chuong2/activity_checkout.png": activity_checkout,
    # Chương 4
    "Hinhve/Chuong4/package_diagram.png": package_diagram,
    "Hinhve/Chuong4/apicore_detail.png": apicore_detail,
    "Hinhve/Chuong4/class_diagram.png": class_diagram,
    "Hinhve/Chuong4/seq_checkout.png": seq_checkout,
    "Hinhve/Chuong4/seq_auth.png": seq_auth,
    "Hinhve/Chuong4/er_diagram.png": er_diagram,
    # Chương 5
    "Hinhve/Chuong5/seq_tenant_context.png": seq_tenant_context,
    "Hinhve/Chuong5/zero_file_render.png": zero_file_render,
    "Hinhve/Chuong5/template_layered_config.png": template_layered_config,
}

if __name__ == "__main__":
    for path, src in DIAGRAMS.items():
        generate(src, path)
