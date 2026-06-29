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

import os
import subprocess
import urllib.request

# Render cục bộ bằng plantuml.jar + font DejaVu Sans. Đây là điểm mấu chốt:
# server kroki không có font phủ đủ dấu tiếng Việt nên các ký tự ghép dấu (ể,
# ấ, ệ, ờ...) bị rơi mất. DejaVu Sans cài sẵn trên máy có đủ glyph nên render
# cục bộ cho chữ tiếng Việt chính xác. Layout dùng engine Smetana tích hợp của
# PlantUML để không phụ thuộc Graphviz (dot). Xuất PNG độ phân giải cao.
PLANTUML_JAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "plantuml.jar")
PLANTUML_URL = "https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar"

STYLE = """!pragma layout smetana
skinparam dpi 300
skinparam defaultFontName "DejaVu Sans"
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontSize 13
"""

SEQ_STYLE = STYLE + """skinparam sequenceMessageAlign center
autonumber
"""


def ensure_jar():
    if os.path.exists(PLANTUML_JAR):
        return
    os.makedirs(os.path.dirname(PLANTUML_JAR), exist_ok=True)
    print(f"... tải plantuml.jar về {PLANTUML_JAR}")
    req = urllib.request.Request(PLANTUML_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(PLANTUML_JAR, "wb") as f:
        f.write(r.read())


def generate(puml, filename):
    # filename kết thúc bằng .png; ghi nguồn .puml cạnh đó rồi gọi plantuml.jar.
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    puml_path = filename[:-4] + ".puml"
    with open(puml_path, "w", encoding="utf-8") as f:
        f.write(puml)
    try:
        # PLANTUML_LIMIT_SIZE mặc định 4096 px khiến các sơ đồ rộng (nhiều
        # swimlane) hoặc dài (luồng nhiều bước) bị cắt cụt. Nâng giới hạn lên để
        # render đầy đủ; các sơ đồ rộng sẽ được đặt trên trang ngang (landscape)
        # trong báo cáo để chữ đủ lớn.
        subprocess.run(
            ["java", "-DPLANTUML_LIMIT_SIZE=16384", "-jar", PLANTUML_JAR,
             "-tpng", "-charset", "UTF-8", puml_path],
            check=True, capture_output=True, text=True,
        )
        os.remove(puml_path)
        print(f"OK   {filename}")
    except subprocess.CalledProcessError as e:
        print(f"FAIL {filename}: {e.stderr}")


# ============================================================
# CHƯƠNG 2 — USE CASE
# ============================================================

usecase_tong_quat = """@startuml
left to right direction
""" + STYLE + """skinparam packageStyle rectangle
actor "Quản trị nền tảng\\n(Platform Admin)" as Admin
actor "Chủ cửa hàng\\n(Tenant Owner)" as Tenant
actor "Khách hàng\\n(End Customer)" as Customer

rectangle "Hệ thống ShopVolo v2" {
  usecase "UC-02: Quản lý master template" as UC02
  usecase "UC-01: Khởi tạo cửa hàng" as UC01
  usecase "UC-03: Tùy biến giao diện\\nvà thương hiệu" as UC03
  usecase "UC-04: Quản lý sản phẩm" as UC04
  usecase "UC-05: Thiết lập menu điều hướng" as UC05
  usecase "UC-06: Tạo trang nội dung động" as UC06
  usecase "UC-10: Ánh xạ tên miền tùy chỉnh" as UC10

  usecase "UC-07: Duyệt sản phẩm\\ntrên trang cửa hàng" as UC07
  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "UC-09: Thanh toán và\\nxử lý đơn hàng" as UC09
}

Admin -- UC02

Tenant -- UC01
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

rectangle "Phân hệ Quản lý và cấu hình cửa hàng" {
  usecase "UC-01: Khởi tạo cửa hàng" as UC01
  usecase "Chọn mẫu giao diện\\ntheo ngành hàng" as UCtpl
  usecase "UC-03: Tùy biến giao diện\\nvà thương hiệu" as UC03
  usecase "Lưu bản nháp bố cục" as UCdraft
  usecase "Xuất bản giao diện" as UCpub
  usecase "UC-05: Thiết lập menu điều hướng" as UC05
  usecase "UC-06: Tạo trang nội dung động" as UC06
  usecase "UC-10: Ánh xạ tên miền tùy chỉnh" as UC10
  usecase "Xác minh tên miền" as UCverify
}

Tenant -- UC01
Tenant -- UC03
Tenant -- UC05
Tenant -- UC06
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
  usecase "UC-07: Duyệt sản phẩm\\ntrên trang cửa hàng" as UC07
  usecase "Xem trang nội dung động\\n(do chủ cửa hàng tạo)" as UCcontent
  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "Lọc theo danh mục\\nvà khoảng giá" as Filter
  usecase "Tìm kiếm sản phẩm" as Search
}

Customer -- UC07
Customer -- UCcontent
Customer -- UC08
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
:Gửi POST /api/shops\\n(qua ứng dụng Admin);
|API Core|
:Tạo bản ghi Shop (PostgreSQL),\\nxóa cache danh sách shop;
if (Bố cục còn trống?) then (đúng)
  :Gieo bố cục\\nmặc định (MongoDB);
else (đã có)
  :Bỏ qua\\n(lũy đẳng);
endif
|Chủ cửa hàng|
:Kéo thả tùy biến\\n(lưu draftData);
:Bấm xuất bản;
|API Core|
:Sao chép draftData\\nsang publishedData;
|Khách hàng|
:Truy cập tên miền cửa hàng;
:proxy.ts phân giải cửa hàng,\\nviết lại path nội bộ;
:Tải publishedData, kết xuất\\ngiao diện động (RSC);
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
if (Kích thước tệp > 10MB?) then (đúng)
  :Trả lỗi 400:\\nvượt giới hạn 10MB;
  |Chủ cửa hàng|
  :Nhận thông báo lỗi;
  stop
endif
|API Core|
:Đọc magic bytes,\\nxác định MIME thực của tệp;
if (Không phải ảnh hợp lệ?) then (đúng)
  :Trả lỗi 400:\\nloại tệp không hợp lệ;
  |Chủ cửa hàng|
  :Nhận thông báo lỗi;
  stop
endif
|API Core|
:Trích kích thước (sharp),\\nsinh BlurHash giữ chỗ;
|Hạ tầng lưu trữ|
:Ghi object vào MinIO;
|API Core|
:Lưu bản ghi Media:\\nURL, kích thước, BlurHash;
|Chủ cửa hàng|
:Nhận URL ảnh\\nvà BlurHash;
note right
  imgproxy resize ảnh
  on-the-fly khi hiển thị,
  không lưu sẵn nhiều
  phiên bản kích thước.
end note
stop
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
:Xác định danh sách hàng\\n(đọc giỏ server-side nếu request thiếu);
:Nạp giá Variant theo shopId; kiểm tra\\nkhuyến mãi, phí vận chuyển và\\nphương thức thanh toán của cửa hàng;
partition "Giao dịch nguyên tử (PostgreSQL)" {
  :Trừ tồn kho và ghi lượt dùng khuyến mãi;
  if (Thanh toán bằng ví?) then (có)
    :Trừ số dư ví\\n(thiếu thì rollback toàn bộ);
  endif
  :Tạo Order, LineItem, Payment, Shipment\\nvà xóa giỏ hàng;
}
if (Chuyển khoản ngân hàng?) then (có)
  :Sinh token xác nhận 24 giờ\\nvà mã QR (ngoài giao dịch);
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
  [admin] as admin
  [storefront] as storefront
  [api-core] as apicore
  [cli-tool] as cli
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
storefront ..> schema
uireg ..> schema
apicore ..> db
cli ..> mtpl

admin --> apicore : REST
storefront --> apicore : REST
storefront ..> imgproxy : URL ảnh

db ..> pg : Prisma
db ..> mongo : Mongoose
apicore ..> redis : cache
apicore ..> minio : S3
imgproxy ..> minio
@enduml
"""

apicore_detail = """@startuml
""" + STYLE + """skinparam packageStyle rectangle

package "api-core (NestJS)" {
  package "Tầng Middleware / Guard" {
    [TenantMiddleware] as tmw
    [BetterAuthGuard] as guard
  }
  package "Tầng Controller" {
    [Controllers\\n(Order, Layout, Shop)] as ctrl
  }
  package "Tầng Service" {
    [OrderService] as osvc
    [LayoutService] as lsvc
    [AuthService] as asvc
    [TenantService\\n(AsyncLocalStorage)] as tsvc
  }
  package "Tầng truy cập dữ liệu" {
    [PrismaService] as prisma
    [Mongoose Models] as mongoose
  }
}

database "Redis" as redis
database "PostgreSQL" as pg
database "MongoDB" as mongo

' Xếp các service thành hai cột cho gọn
osvc -[hidden]right- asvc
lsvc -[hidden]right- tsvc

tmw --> guard
tmw --> tsvc : run({shopId})
tmw --> redis : tra cứu domain
guard --> asvc : kiểm tra phiên
guard --> ctrl

ctrl --> osvc
ctrl --> lsvc

osvc --> tsvc : getTenantId()
lsvc --> tsvc : getTenantId()

osvc --> prisma
asvc --> prisma
lsvc --> mongoose

prisma --> pg
mongoose --> mongo
redis -[hidden]down- pg
@enduml
"""

class_diagram = """@startuml
""" + STYLE + """skinparam classAttributeIconSize 0
hide circle

class TenantMiddleware {
  - tenantService
  - prisma
  - cacheManager
  + use(req, res, next)
}

class BetterAuthGuard {
  - authService
  - prisma
  - cacheManager
  + canActivate(context)
}

class OrderService {
  - prisma
  - tenantService
  - inventoryService
  + createOrder(customerId, dto)
  + cancelOrder(id, customerId?)
  + refundOrder(id)
}

class LayoutService {
  - tenantService
  - globalLayoutModel
  - pageLayoutModel
  + getPageLayout(shopId, type)
  + publishLayoutByShopId(shopId)
  + seedDefaultLayouts(shopId)
}

class TenantService {
  - {static} als: AsyncLocalStorage
  + run(context, callback)
  + getTenantId()
}

class AuthService {
  - prisma
  + getOwnerSession(req)
  + getCustomerSession(req)
  + login(dto)
}

class PrismaService {
  + onModuleInit()
  + $transaction(fn)
}

' Hai cột: trái = thành phần nghiệp vụ, phải = hạ tầng dùng chung
TenantMiddleware -[hidden]down- BetterAuthGuard
BetterAuthGuard -[hidden]down- OrderService
OrderService -[hidden]down- LayoutService
TenantService -[hidden]down- AuthService
AuthService -[hidden]down- PrismaService

TenantMiddleware ..> TenantService : <<use>>
TenantMiddleware ..> PrismaService : <<use>>
BetterAuthGuard ..> AuthService : <<use>>
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
participant "__:PrismaService__" as PR

KH -> OC : POST /orders/checkout
activate OC
OC -> OS : createOrder(dto)
activate OS
OS -> PR : variant.findMany\\n({id, shopId})
activate PR
PR --> OS : Variant kèm giá
deactivate PR

opt có promotionCode
  OS -> PR : promotion.findFirst\\n({shopId, code})
  activate PR
  PR --> OS : khuyến mãi
  deactivate PR
end

OS -> PR : $transaction(fn)
activate PR
alt đủ tồn kho và số dư
  PR -> PR : decrementStock()
  PR -> PR : order.create()\\n+ payment + shipment
  PR -> PR : cartItem.deleteMany()
  PR --> OS : Order {id, number}
else thiếu kho / số dư
  PR --> OS : rollback toàn bộ
end
deactivate PR

OS ->> OS : gửi thông báo\\n+ email (bất đồng bộ)
OS --> OC : finalOrder\\n(kèm QR nếu CK)
deactivate OS
OC --> KH : 201 / 400
deactivate OC
@enduml
"""

seq_auth = """@startuml
""" + SEQ_STYLE + """
actor "Người dùng" as ND
participant "__:BetterAuthGuard__" as G
participant "__:AuthService__" as AS
participant "__:PrismaService__" as PR

ND -> G : HTTP Request\\n(cookie phiên)
activate G

alt endpoint @Public()
  G --> ND : cho qua
else cần xác thực
  G -> AS : getOwnerSession(req)
  activate AS
  AS -> AS : better-auth\\napi.getSession()
  AS --> G : {user, session}\\nhoặc null
  deactivate AS

  alt phiên hợp lệ
    G -> PR : shop.findMany\\n({ownerId})
    activate PR
    PR --> G : danh sách shopId
    deactivate PR
    G --> ND : canActivate = true
  else phiên không hợp lệ
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
participant "__:OrderService__" as OS

KH -> TM : GET /api/...\\n(Host: duck.myapp.com)
activate TM
TM -> TM : bóc tách "duck"
TM -> RD : get("domain:duck")
activate RD
RD --> TM : kết quả cache
deactivate RD

alt trượt cache
  TM -> PR : shop.findUnique\\n({domain})
  activate PR
  PR --> TM : {id, status}
  deactivate PR
  TM -> RD : set(domain, 300s)
end

opt status = SUSPENDED
  TM --> KH : HTTP 403
end

TM -> TS : run({shopId}, next)
activate TS
TS -> OS : xử lý trong\\nvùng ngữ cảnh
activate OS
OS -> TS : getTenantId()
TS --> OS : shopId
OS -> PR : truy vấn\\ntheo shopId
activate PR
PR --> OS : dữ liệu đúng\\ncửa hàng
deactivate PR
OS --> KH : HTTP Response
deactivate OS
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

activity_draft_publish = """@startuml
""" + STYLE + """
|Chủ cửa hàng|
start
:Mở trình thiết kế kéo thả;
:Tải draftData\\n(trống thì sao từ publishedData);
repeat
  :Kéo thả, chỉnh thuộc tính;
  :Lưu draftData\\n(POST /layouts/builder/save);
  :Xem trước máy tính / di động;
repeat while (Còn chỉnh sửa?) is (có)
->không;
:Bấm xuất bản;
|API Core|
:Sao chép nguyên tử\\ndraftData -> publishedData\\n(từng trang hoặc bulkWrite);
:Vô hiệu hóa cache bố cục\\ntheo nhãn cửa hàng;
|Khách hàng|
:Lần truy cập kế tiếp nhận\\nbản giao diện mới;
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
# CHƯƠNG 4 — THIẾT KẾ TÀI LIỆU MONGODB (MongoDB Atlas)
# ============================================================

mongo_design = """@startuml
""" + STYLE + """skinparam classAttributeIconSize 0
hide circle
hide methods

class "GlobalLayout (collection)" as GL {
  _id : ObjectId
  shopId : string <<index>>
  draftData : object
  publishedData : object
  updatedAt : date
}

class "PageLayout (collection)" as PL {
  _id : ObjectId
  shopId : string <<index>>
  pageType : string  /' home | product-list | product-detail '/
  slug : string
  draftData : object
  publishedData : object
}

class "publishedData / draftData" as DATA {
  theme : { colors, fonts }
  header : UIComponentRef[]
  footer : UIComponentRef[]
  components : UIComponentRef[]
}

class "UIComponentRef (sub-document)" as REF {
  componentId : string
  props : object
  blocks : UIComponentRef[]  /' đệ quy '/
}

class "MasterTemplateCatalog (collection)" as MTC {
  _id : ObjectId
  industry : string  /' thời trang, điện tử... '/
  templateKey : string
  isCustom : boolean
  layout : object
}

class "UIComponentCatalog (collection)" as UCC {
  _id : ObjectId
  componentId : string
  propSchema : object  /' lược đồ sinh form '/
}

GL *-- DATA : nhúng
PL *-- DATA : nhúng
DATA *-- REF : danh sách
REF *-- REF : blocks (lồng nhau)
MTC ..> DATA : gieo lúc khởi tạo
UCC ..> REF : kiểm soát props

legend bottom left
  Mỗi cửa hàng (shopId) tương ứng một bộ tài liệu bố cục trong MongoDB.
  Cấu trúc lồng nhau, không cần schema cố định, lưu đồng thời hai phiên bản
  draft (đang sửa) và published (đang chạy) trong cùng một tài liệu.
endlegend
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
    "Hinhve/Chuong4/mongo_design.png": mongo_design,
    # Chương 5
    "Hinhve/Chuong5/seq_tenant_context.png": seq_tenant_context,
    "Hinhve/Chuong5/zero_file_render.png": zero_file_render,
    "Hinhve/Chuong5/template_layered_config.png": template_layered_config,
    "Hinhve/Chuong5/activity_draft_publish.png": activity_draft_publish,
}

if __name__ == "__main__":
    ensure_jar()
    for path, src in DIAGRAMS.items():
        generate(src, path)
