import urllib.request, zlib, base64

def encode_plantuml(text):
    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).decode('utf-8').replace('+','-').replace('/','_').replace('=','')

def generate(puml, filename):
    url = "http://www.plantuml.com/plantuml/png/" + encode_plantuml(puml)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Successfully generated {filename}")
    except Exception as e:
        print(f"Failed to generate {filename}: {e}")

puml_tong_quat = """@startuml
left to right direction
skinparam packageStyle rectangle
actor "Tenant Owner" as Tenant
actor "End Customer" as Customer

rectangle "ShopVolo v2" {
  usecase "UC-01: Khởi tạo Shop" as UC01
  usecase "UC-02: Quản lý Khuyến mãi" as UC02
  usecase "UC-03: Tùy biến thương hiệu" as UC03
  usecase "UC-04: Quản lý sản phẩm" as UC04
  usecase "UC-05: Thiết lập menu" as UC05
  usecase "UC-10: Ánh xạ tên miền" as UC10
  
  usecase "UC-06: Xem trang nội dung" as UC06
  usecase "UC-07: Duyệt sản phẩm động" as UC07
  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "UC-09: Thanh toán & đơn hàng" as UC09
}

Tenant -- UC01
Tenant -- UC02
Tenant -- UC03
Tenant -- UC04
Tenant -- UC05
Tenant -- UC10

Customer -- UC06
Customer -- UC07
Customer -- UC08
Customer -- UC09
@enduml
"""

puml_quan_ly_shop = """@startuml
left to right direction
skinparam packageStyle rectangle
actor "Tenant Owner" as Tenant

rectangle "Quản lý Shop" {
  usecase "UC-01: Khởi tạo Shop" as UC01
  usecase "UC-02: Quản lý Khuyến mãi" as UC02
  usecase "UC-03: Tùy biến thương hiệu" as UC03
  usecase "UC-05: Thiết lập menu" as UC05
  usecase "UC-10: Ánh xạ tên miền" as UC10
}

Tenant -- UC01
Tenant -- UC02
Tenant -- UC03
Tenant -- UC05
Tenant -- UC10
@enduml
"""

puml_san_pham_don_hang = """@startuml
left to right direction
skinparam packageStyle rectangle
actor "Tenant Owner" as Tenant
actor "End Customer" as Customer

rectangle "Sản phẩm & Đơn hàng" {
  usecase "UC-04: Quản lý sản phẩm" as UC04
  usecase "Thêm mới sản phẩm" as AddProduct
  usecase "Phân loại sản phẩm" as CatProduct
  usecase "Định giá sản phẩm" as PriceProduct
  usecase "Kiểm soát tồn kho" as Inventory
  
  usecase "UC-08: Quản lý giỏ hàng" as UC08
  usecase "UC-09: Thanh toán & đơn hàng" as UC09
}

Tenant -- UC04
UC04 .> AddProduct : <<include>>
UC04 .> CatProduct : <<include>>
UC04 .> PriceProduct : <<include>>
UC04 .> Inventory : <<include>>

Customer -- UC08
Customer -- UC09
@enduml
"""

puml_khach_hang = """@startuml
left to right direction
skinparam packageStyle rectangle
actor "End Customer" as Customer

rectangle "Trải nghiệm Khách hàng" {
  usecase "UC-06: Xem trang nội dung" as UC06
  usecase "UC-07: Duyệt sản phẩm động" as UC07
  usecase "Lọc sản phẩm" as Filter
  usecase "Tìm kiếm thời gian thực" as Search
}

Customer -- UC06
Customer -- UC07
Filter .> UC07 : <<extend>>
Search .> UC07 : <<extend>>
@enduml
"""

generate(puml_tong_quat, "Hinhve/Chuong2/usecase_tong_quat.png")
generate(puml_quan_ly_shop, "Hinhve/Chuong2/usecase_quan_ly_shop.png")
generate(puml_san_pham_don_hang, "Hinhve/Chuong2/usecase_san_pham_don_hang.png")
generate(puml_khach_hang, "Hinhve/Chuong2/usecase_khach_hang.png")
