# GUIDE VIẾT CHƯƠNG 4 — ShopVolo v2
> **Dành cho AI agent thực thi.** Đọc toàn bộ trước khi chỉnh sửa bất kỳ dòng LaTeX nào.
> **Nguồn sự thật:** `4_Ket_qua_thuc_nghiem.tex` (template), `2_Khao_sat.tex` (labels & UC), `3_Cong_nghe.tex` (stack), `5_Giai_phap_dong_gop.tex` (deep_merge label).

---

## 0. NGUYÊN TẮC BẮT BUỘC

1. **Bám sát template gốc** — Giữ nguyên đúng 5 `\section` và tên các `\subsection` trong `4_Ket_qua_thuc_nghiem.tex`. Không đổi tên, không bỏ section, không thêm section mới.
2. **Xóa văn bản hướng dẫn gốc** — Khi viết từng subsection, xóa toàn bộ các đoạn hướng dẫn của giảng viên (bắt đầu bằng "Mục này có độ dài...", "Sinh viên cần...", "SV tham khảo..."). Thay bằng nội dung thực.
3. **Xóa hình ví dụ của giảng viên** — Xóa cả hai hình `Picture1.png` / `fig:Fig1` và `Picture2.png` / `fig:Fig2` cùng đoạn mô tả "Ví dụ biểu đồ..." ra khỏi file cuối.
4. **Không bullet trong văn bản LaTeX** — Viết thành đoạn văn hoàn chỉnh, đủ chủ-vị. Khi liệt kê dùng `(i), (ii), (iii)` trong câu văn.
5. **Mọi hình/bảng đều phải được `\ref{}` trong văn bản** trước hoặc ngay sau hình/bảng đó. Không có hình "mồ côi".
6. **Placeholder `[ĐIỀN_...]`** — Mọi số liệu chưa có (LOC, test pass/fail, dung lượng bundle) để dạng `[ĐIỀN_...]`. Không bịa số.
7. **Giọng văn học thuật** — Bị động / ngôi thứ ba. Ví dụ: *"Hệ thống được thiết kế theo..."*, *"Biểu đồ thể hiện..."*.
8. **Phụ lục A** — Thêm nội dung lớp bổ sung vào CUỐI file `Chuong/Phu_luc_A.tex`, SAU tất cả các `\section` hiện có. Không thêm vào giữa file.

---

## 1. THÔNG TIN DỰ ÁN (context cứng — KHÔNG thay đổi)

| Thuộc tính | Giá trị |
|---|---|
| Tên hệ thống | ShopVolo v2 |
| Loại | Multi-tenant SaaS thương mại điện tử |
| Kiến trúc | **MVC** |
| Monorepo | Turborepo 2.x |
| Apps | `api` (NestJS 11.x), `storefront` (Next.js 15.x), `dashboard` (Next.js 15.x), `admin` (Next.js 15.x) |
| Packages | `@repo/database`, `@repo/auth`, `@repo/config`, `@repo/ui`, `@repo/utils` |
| DB chính | PostgreSQL 16 + Prisma **5.x** |
| DB phụ | MongoDB 7 + Mongoose 8.x |
| Cache | Redis 7.x — **TTL = 3600 giây (1 giờ)** |
| Storage | MinIO |
| Auth | Better Auth 1.x |
| Styling | Tailwind CSS 4.x |
| Validation | Zod 3.x |
| Container | Docker 26.x + Kubernetes 1.29+ |
| Ngôn ngữ | TypeScript 5.x (Node 20 LTS) |

### Ánh xạ MVC vào ShopVolo v2

| MVC | Vai trò | Ánh xạ cụ thể |
|---|---|---|
| **Model (M)** | Dữ liệu & logic nghiệp vụ | Prisma models + Mongoose schemas trong `@repo/database`; NestJS Services (TenantService, OrderService…) |
| **View (V)** | Giao diện người dùng | Apps `storefront`, `dashboard`, `admin` (Next.js 15 — Server Components + Client Components) |
| **Controller (C)** | Điều phối request/response | NestJS Controllers trong `api`; Next.js Route Handlers (BFF) trong frontend apps |

---

## 2. LABELS — BẢNG TRA CỨU ĐẦY ĐỦ

### Labels đã tồn tại trong Ch.2 (dùng `\ref{}`, KHÔNG khai báo lại)

```
% Hình từ 2_Khao_sat.tex (dùng _ không dùng -)
\ref{fig:usecase_tong_quat}        % §2.2.1  usecase_tong_quat.png
\ref{fig:usecase_quan_ly_shop}     % §2.2.2
\ref{fig:usecase_san_pham_don_hang}% §2.2.3
\ref{fig:usecase_khach_hang}       % §2.2.4
\ref{fig:activity_onboarding}      % §2.2.5  activity_onboarding.png
\ref{fig:activity_upload_product}  % §2.3.3  activity_upload_product.png
\ref{fig:activity_checkout}        % §2.3.5  activity_checkout.png

% Bảng use case từ 2_Khao_sat.tex
\ref{table:uc01}    % §2.3.1 UC-01 Onboarding
\ref{table:uc03}    % §2.3.2 UC-03 Branding
\ref{table:uc04}    % §2.3.3 UC-04 Product
\ref{table:uc07}    % §2.3.4 UC-07 Dynamic Rendering
\ref{table:uc09}    % §2.3.5 UC-09 Checkout

% Section labels từ 2_Khao_sat.tex
\ref{section:2.4}           % Yêu cầu phi chức năng
\ref{subsection:2.3.5}      % Đặc tả UC-09
```

### Labels đã tồn tại trong Ch.5 (dùng `\ref{}`, KHÔNG khai báo lại)

```
\ref{fig:deep_merge_flow}   % Khai báo trong 5_Giai_phap_dong_gop.tex
```

### Labels mới cần khai báo trong Ch.4 (dùng `\label{}` + `\ref{}`)

```latex
% §4.1
\label{section:4.1}
\label{subsection:4.1.1}
\label{subsection:4.1.2}
\label{subsection:4.1.3}
\label{fig:pkg_overview}         % Package diagram tổng quan
\label{fig:pkg_detail_core}      % Package detail: core packages
\label{fig:pkg_detail_apps}      % Package detail: apps

% §4.2
\label{section:4.2}
\label{subsection:4.2.1}
\label{subsection:4.2.2}
\label{subsection:4.2.3}
\label{fig:ui_storefront}        % UI placeholder storefront
\label{fig:ui_dashboard}         % UI placeholder dashboard
\label{fig:class_tenant}         % Class diagram TenantService
\label{fig:class_storefront}     % Class diagram StorefrontConfigResolver
\label{fig:class_order}          % Class diagram OrderService
\label{fig:class_middleware}     % Class diagram TenantMiddleware
\label{fig:seq_uc01}             % Sequence UC-01
\label{fig:seq_uc04}             % Sequence UC-04
\label{fig:seq_uc07}             % Sequence UC-07
\label{fig:er_postgres}          % E-R PostgreSQL
\label{fig:er_mongo}             % Schema MongoDB

% §4.3
\label{section:4.3}
\label{subsection:4.3.1}
\label{subsection:4.3.2}
\label{subsection:4.3.3}
\label{table:tools}              % Bảng công cụ
\label{table:stats}              % Bảng thống kê LOC

% §4.4
\label{section:4.4}
\label{table:tc_uc01}            % Test case UC-01
\label{table:tc_uc07}            % Test case UC-07

% §4.5
\label{section:4.5}
```

---

## 3. SECTION §4.1 — THIẾT KẾ KIẾN TRÚC

### Đoạn mở đầu chương (TRƯỚC section đầu tiên)

**[VIẾT VĂN XUÔI]** Đoạn liên kết từ Chương 3: Chương 3 đã trình bày và luận giải các công nghệ được lựa chọn. Chương 4 tập trung trình bày toàn bộ quá trình thiết kế kiến trúc, thiết kế chi tiết, xây dựng và kiểm thử hệ thống. Phần `\ref{section:4.1}` trình bày thiết kế kiến trúc MVC. Phần `\ref{section:4.2}` đi sâu vào giao diện, lớp và cơ sở dữ liệu. Phần `\ref{section:4.3}` mô tả kết quả xây dựng. Phần `\ref{section:4.4}` trình bày kiểm thử. Phần `\ref{section:4.5}` đề cập triển khai.

---

### §4.1.1 `\subsection{Lựa chọn kiến trúc phần mềm}` — Độ dài 1–3 trang

**[VIẾT VĂN XUÔI — 3 đoạn văn]**

**Đoạn 1 — Giới thiệu MVC:**
Giải thích ngắn gọn kiến trúc MVC (không quá nửa trang): MVC phân chia ứng dụng thành 3 thành phần có trách nhiệm riêng biệt. Nêu ưu điểm: tách biệt trách nhiệm, kiểm thử độc lập, bảo trì dễ khi mở rộng.

**Đoạn 2 — Ánh xạ MVC vào ShopVolo v2:**
Mô tả chi tiết cách từng thành phần MVC được hiện thực hóa. Dùng bảng ánh xạ ở mục 1 trên, chuyển thành văn xuôi. Đặc biệt nhấn mạnh Model gồm 2 tầng: (i) tầng dữ liệu trong `@repo/database`, (ii) tầng nghiệp vụ là các NestJS Service.

**Đoạn 3 — Điểm bổ sung so với MVC chuẩn:**
Hệ thống bổ sung 2 cơ chế: (i) `TenantMiddleware` hoạt động trước Controller, trích xuất tenant từ subdomain/header; (ii) tầng cache Redis giữa Controller và Model, đáp ứng mục tiêu phản hồi dưới 10ms khi cache warm đã đặt ra tại `\ref{section:2.4}`.

---

### §4.1.2 `\subsection{Thiết kế tổng quan}`

**Hình cần vẽ:** `fig:pkg_overview` — Package Diagram 3 tầng

**File ảnh:** `Hinhve/pkg_overview.png` ← vẽ bằng draw.io, export PNG

**Blueprint bố cục (từ trên xuống):**

```
TẦNG GIAO DIỆN (Presentation Layer)
  «app» storefront | «app» dashboard | «app» admin

  ↓ «use» (HTTP/REST)

TẦNG ĐIỀU PHỐI (Controller Layer)
  «app» api  (NestJS Controllers + Route Handlers)

  ↓ «use»

TẦNG MODEL & SHARED (Model + Shared Packages)
  «package» @repo/database
  «package» @repo/auth
  «package» @repo/config
  «package» @repo/utils

SHARED UI (dùng bởi tầng View trực tiếp)
  «package» @repo/ui
```

**Quan hệ phụ thuộc (mũi tên `«use»`):**
- `storefront`, `dashboard`, `admin` → `api` (qua HTTP)
- `api` → `@repo/database`, `@repo/auth`, `@repo/config`, `@repo/utils`
- `storefront`, `dashboard`, `admin` → `@repo/ui`, `@repo/config`, `@repo/utils`
- **KHÔNG có mũi tên ngược.** Tầng dưới không phụ thuộc tầng trên.

**Lệnh LaTeX:**
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{Hinhve/pkg_overview.png}
    \caption{Biểu đồ gói UML tổng quan hệ thống ShopVolo v2}
    \label{fig:pkg_overview}
\end{figure}
```

**[VIẾT VĂN XUÔI sau hình]** Mô tả 3 tầng và 9 package theo đúng bảng ánh xạ. Giải thích mục đích từng package (không dùng bullet — viết thành đoạn văn liên tục).

---

### §4.1.3 `\subsection{Thiết kế chi tiết gói}`

#### Hình 1: `fig:pkg_detail_core` — Nhóm packages lõi

**File ảnh:** `Hinhve/pkg_detail_core.png`

**Các lớp cần có (chỉ tên, không attrs/methods):**

```
@repo/database:
  PostgreSQL (Prisma): TenantModel, ShopModel, UserModel,
    ProductModel, OrderModel, OrderItemModel, ThemeModel, TemplateModel
    PrismaClient (singleton)
  MongoDB (Mongoose): LayoutDocument, ComponentRegistryDocument,
    AnalyticsEventDocument, MongooseConnection (singleton)

@repo/auth:  AuthClient, SessionValidator, TenantMiddleware

@repo/utils: DeepMergeUtil, SlugGenerator, DateFormatter

@repo/config: AppConfig, EnvLoader
```

**6 quan hệ UML cần thể hiện trong hình này:**

| # | Loại | Ví dụ trong hình | Ký hiệu |
|---|---|---|---|
| 1 | **Dependency** | `TenantMiddleware` → `AuthClient` | `- - →` |
| 2 | **Association** | `PrismaClient` — `TenantModel` | `——→` |
| 3 | **Aggregation** | `MongooseConnection` ◇— `LayoutDocument` | `◇——` |
| 4 | **Dependency** (sửa từ Composition) | `AppConfig` - - → `EnvLoader` | `- - →` |
| 5 | **Inheritance** | `LayoutDocument` △— `ComponentRegistryDocument` | `△——` |
| 6 | **Implementation** | `JwtGuard` △- - - `CanActivate` (NestJS interface) | `△- - -` |

> ⚠️ **Lưu ý đã sửa từ audit:** Quan hệ 4 là **Dependency**, KHÔNG phải Composition. `AppConfig` phụ thuộc vào `EnvLoader` để khởi tạo. `CanActivate` là interface built-in của NestJS, không phải `IGuard` tự định nghĩa.

**Lệnh LaTeX:**
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{Hinhve/pkg_detail_core.png}
    \caption{Thiết kế chi tiết nhóm packages lõi}
    \label{fig:pkg_detail_core}
\end{figure}
```

#### Hình 2: `fig:pkg_detail_apps` — Nhóm apps

**File ảnh:** `Hinhve/pkg_detail_apps.png`

**Các lớp cần có (chỉ tên):**

```
api (NestJS):
  Controllers: TenantController, ShopController, ProductController,
               OrderController, AuthController, StorefrontConfigController
  Services:    TenantService, ShopService, ProductService, OrderService,
               AuthService, StorefrontConfigService
  Guards/MW:   TenantMiddleware, JwtGuard, RolesGuard

storefront (Next.js):
  StorefrontPage, StorefrontConfigResolver, ComponentResolver,
  DynamicComponentRenderer

dashboard (Next.js):
  DashboardLayout, ProductManagementPage, OrderManagementPage, ThemeEditorPage

admin (Next.js):
  AdminLayout, TenantListPage, SystemConfigPage
```

**Quan hệ cần thể hiện:**
- `TenantController` → `TenantService` (dependency)
- `StorefrontConfigResolver` → `StorefrontConfigController` (dependency, qua HTTP)
- `ComponentResolver` — `StorefrontConfigResolver` (association)
- `StorefrontPage` ◆— `DynamicComponentRenderer` (composition — Page chứa Renderer)
- `JwtGuard` △- - - `CanActivate` (implementation)
- `ProductManagementPage` — `DashboardLayout` (association)

**Lệnh LaTeX:**
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{Hinhve/pkg_detail_apps.png}
    \caption{Thiết kế chi tiết nhóm ứng dụng}
    \label{fig:pkg_detail_apps}
\end{figure}
```

**[VIẾT VĂN XUÔI sau 2 hình]** Giải thích nhóm packages lõi đảm nhận tầng Model. Đề cập `DeepMergeUtil` là cơ chế Zero-file, tham chiếu Chương 5: *"được phân tích chi tiết trong Chương 5"* (không dùng `\ref{chap:5}` vì label đó có thể chưa tồn tại).

---

## 4. SECTION §4.2 — THIẾT KẾ CHI TIẾT

### §4.2.1 `\subsection{Thiết kế giao diện}` — Độ dài 2–3 trang

**[VIẾT VĂN XUÔI — 3 phần]**

**Phần 1 — Đặc tả màn hình:**
```
Desktop: 1440×900px (primary), tối thiểu 1280×720px
Tablet: breakpoint 768px (md)
Mobile: 390×844px (sm)
Màu: sRGB, hỗ trợ Dark Mode (prefers-color-scheme)
Storefront: fluid layout
Dashboard/Admin: sidebar 240px cố định + content flexible
```

**Phần 2 — Chuẩn hóa giao diện (Design Tokens):**
```
Màu:
  Primary:   #6366F1 (Indigo-500) — nút hành động chính
  Secondary: #8B5CF6 (Violet-500) — accent
  Success:   #22C55E (Green-500)  — xác nhận
  Danger:    #EF4444 (Red-500)    — lỗi, xóa
  BG light:  #FFFFFF / #F9FAFB
  BG dark:   #111827 / #1F2937

Typography: Inter (Google Fonts)
  H1: 32px/700 | H2: 24px/600 | Body: 16px/400

Nút:
  Primary: bg-primary, text-white, rounded-md (8px), h=40px
  Secondary: border-primary, transparent bg
  Disabled: opacity-50

Toast notification:
  Vị trí: top-right
  Success: auto-dismiss 3s | Error: manual dismiss 5s

Form validation: lỗi hiển thị dưới input, màu Danger
```

**Phần 3 — Hình ảnh minh họa:**

> ⚠️ **Đã sửa từ audit:** Chỉ dùng `Picture3.png` hoặc `Picture1.png` làm placeholder. **KHÔNG dùng `activity_*.png`** (đó là activity diagram, không phải UI mockup).

```latex
% Hình 1: UI Storefront
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{Hinhve/Picture3.png}
    \caption{Thiết kế giao diện trang storefront động (placeholder — thay bằng screenshot thực)}
    \label{fig:ui_storefront}
\end{figure}
```

```latex
% Hình 2: UI Dashboard
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{Hinhve/Picture3.png}
    \caption{Thiết kế giao diện Dashboard quản lý shop (placeholder — thay bằng screenshot thực)}
    \label{fig:ui_dashboard}
\end{figure}
```

---

### §4.2.2 `\subsection{Thiết kế lớp}` — Độ dài 3–4 trang

> ⚠️ **Đã sửa từ audit:** Giới hạn **4 lớp** (không phải 5). `AuthService` → Phụ lục A.

**4 lớp chủ đạo được chọn:**
1. `TenantService`
2. `StorefrontConfigResolver`
3. `OrderService`
4. `TenantMiddleware`

---

#### Lớp 1: `TenantService`

**File ảnh:** `Hinhve/class_tenant.png` — vẽ class diagram với draw.io

```
Class: TenantService
Package: api/src/tenant/

Attributes (private):
  - prisma: PrismaClient
  - redis: RedisClient
  - minioService: MinioService

Methods (public):
  + register(dto: CreateTenantDto): Promise<Tenant>
  + assignMasterTemplate(tenantId: string): Promise<void>
  + getShopConfig(tenantId: string): Promise<ShopConfig>
  + updateBranding(tenantId: string, dto: UpdateBrandingDto): Promise<Shop>
  + invalidateCache(tenantId: string): Promise<void>

Methods (private):
  - generateSlug(name: string): string
  - validateDomain(domain: string): Promise<boolean>
```

**[VIẾT VĂN XUÔI]** Mô tả TenantService là lớp nghiệp vụ trung tâm quản lý vòng đời tenant. Nhấn mạnh cơ chế invalidateCache được gọi sau mỗi cập nhật cấu hình để đảm bảo tính nhất quán Redis–MongoDB.

---

#### Lớp 2: `StorefrontConfigResolver`

**File ảnh:** `Hinhve/class_storefront.png`

```
Class: StorefrontConfigResolver
Package: storefront/src/lib/

Attributes (private):
  - apiBaseUrl: string
  - cacheTimeout: number  (= 3600)

Methods (public):
  + resolve(domain: string): Promise<StorefrontConfig>
  + mergeThemeOverrides(base: ThemeConfig, override: Partial<ThemeConfig>): ThemeConfig

Methods (private):
  - fetchFromApi(domain: string): Promise<RawConfig>
  - validateConfig(config: unknown): StorefrontConfig
```

**[VIẾT VĂN XUÔI]** Mô tả vai trò cầu nối View–Model. Nhấn mạnh `mergeThemeOverrides` gọi `DeepMergeUtil`, tham chiếu Chương 5 cho thuật toán chi tiết.

---

#### Lớp 3: `OrderService`

**File ảnh:** `Hinhve/class_order.png`

```
Class: OrderService
Package: api/src/order/

Attributes (private):
  - prisma: PrismaClient
  - paymentGateway: IPaymentGateway
  - eventEmitter: EventEmitter2

Methods (public):
  + createOrder(dto: CreateOrderDto): Promise<Order>
  + processWebhook(payload: WebhookPayload, signature: string): Promise<void>
  + verifySignature(payload: string, signature: string, secret: string): boolean
  + getOrdersByTenant(tenantId: string, query: PaginationDto): Promise<PaginatedOrders>
  + updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order>

Methods (private):
  - calculateTotal(items: OrderItem[]): number
  - emitOrderEvent(event: OrderEvent): void
```

**[VIẾT VĂN XUÔI]** Mô tả vòng đời đơn hàng. Nhấn mạnh `verifySignature` dùng HMAC-SHA256 chống giả mạo webhook (tham chiếu `\ref{table:uc09}` và `\ref{subsection:2.3.5}`).

---

#### Lớp 4: `TenantMiddleware`

**File ảnh:** `Hinhve/class_middleware.png`

```
Class: TenantMiddleware
Package: api/src/common/middleware/
Implements: NestMiddleware (NestJS built-in)

Attributes (private):
  - tenantService: TenantService
  - authService: AuthService

Methods (public):
  + use(req: Request, res: Response, next: NextFunction): Promise<void>

Methods (private):
  - extractTenantId(req: Request): string | null
  - attachTenantContext(req: Request, tenant: Tenant): void
```

**[VIẾT VĂN XUÔI]** Giải thích middleware đăng ký toàn cục, hoạt động trước mọi Controller, trích xuất tenant từ subdomain/header và gắn vào `req.tenant`. Toàn bộ Controller bên dưới chỉ đọc `req.tenant`, đảm bảo cô lập dữ liệu giữa các tenant.

---

#### Sequence Diagram 1: UC-01 — Khởi tạo Shop

**File ảnh:** `Hinhve/seq_uc01.png`

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{Hinhve/seq_uc01.png}
    \caption{Biểu đồ trình tự UC-01 — Khởi tạo Shop (Tenant Onboarding)}
    \label{fig:seq_uc01}
\end{figure}
```

**Actors/Objects:** `NewUser` → `:AuthController` → `:AuthService` → `:TenantService` → `:PrismaClient` → `:TemplateModel` → `:RedisClient`

**Luồng chính (đúng thứ tự):**
```
1. NewUser → AuthController: POST /auth/register {email, password, shopName}
2. AuthController → AuthService: register(dto)
3. AuthService → PrismaClient: createUser(email, hashedPassword)
   PrismaClient → AuthService: userId
4. AuthService → TenantService: register({userId, shopName})
5. TenantService → PrismaClient: createTenant({shopName, slug})
   PrismaClient → TenantService: tenantId
6. TenantService → TemplateModel: findMasterTemplate()
   TemplateModel → TenantService: masterTemplateId
7. TenantService → PrismaClient: assignTemplate(tenantId, masterTemplateId)
8. TenantService → RedisClient: set(cacheKey, shopConfig, TTL=3600)
9. AuthController → NewUser: 201 Created {tenantId, token}
```

**[VIẾT VĂN XUÔI]** Tham chiếu biểu đồ hoạt động `\ref{fig:activity_onboarding}` và đặc tả `\ref{table:uc01}` để người đọc đối chiếu.

---

#### Sequence Diagram 2: UC-04 — Quản lý sản phẩm + AI xóa nền

**File ảnh:** `Hinhve/seq_uc04.png`

**Actors/Objects:** `TenantUser` → `:ProductController` (với TenantMiddleware đã chạy) → `:ProductService` → `:PrismaClient` → `:MinioService` → `:AIBackgroundRemovalService`

> ⚠️ **Đã sửa từ audit:** Thứ tự đúng: createProduct trong DB **trước**, rồi mới upload ảnh. AI job là **bất đồng bộ** (async), xảy ra sau khi đã trả lời client.

**Luồng chính (thứ tự đúng):**
```
1. TenantUser → ProductController: POST /products {name, price, imageFile}
   [TenantMiddleware đã chạy, req.tenant đã được gắn]
2. ProductController → ProductService: createProduct(dto, req.tenant)
3. ProductService → PrismaClient: createProduct({...dto, tenantId})
   PrismaClient → ProductService: productId
4. ProductService → MinioService: uploadRaw(imageFile)
   MinioService → ProductService: rawImageUrl
5. ProductService → PrismaClient: updateProduct(productId, {imageUrl: rawImageUrl})
6. ProductService → AIBackgroundRemovalService: enqueueJob(productId, rawImageUrl)
   [ASYNC — không chặn luồng chính]
7. ProductController → TenantUser: 201 Created {productId, imageUrl: rawImageUrl}
--- Sau đó, bất đồng bộ ---
8. AIJob → MinioService: uploadProcessed(resultBuffer) → processedUrl
9. AIJob → PrismaClient: updateProduct(productId, {imageUrl: processedUrl})
```

**[VIẾT VĂN XUÔI]** Nhấn mạnh bước 6 là async job queue — ảnh gốc hiển thị ngay cho khách, ảnh AI cập nhật sau. Tham chiếu `\ref{fig:activity_upload_product}` và `\ref{table:uc04}`.

---

#### Sequence Diagram 3: UC-07 — Duyệt sản phẩm động

**File ảnh:** `Hinhve/seq_uc07.png`

> ⚠️ **Đã sửa từ audit:** Phân ranh giới rõ ràng giữa `storefront` app và `api` app. `StorefrontConfigService` là lớp trong `api`, không nằm trong `storefront`.

**Actors/Objects:**
```
[storefront app]: Visitor → :StorefrontPage → :StorefrontConfigResolver → :RedisClient
                                                                         → HTTP GET →
[api app]: :StorefrontConfigController → :StorefrontConfigService → :DeepMergeUtil → :RedisClient
[storefront app]: → :ComponentResolver → :DynamicComponentRenderer → Visitor
```

**Luồng chính:**
```
1. Visitor → StorefrontPage: GET https://{shopDomain}/products/{slug}
2. StorefrontPage → StorefrontConfigResolver: resolve(shopDomain)
3. StorefrontConfigResolver → RedisClient: get(cacheKey)
   [Cache HIT] → cachedConfig → bỏ qua bước 4–6, nhảy đến bước 7
   [Cache MISS] → tiếp tục bước 4
4. StorefrontConfigResolver → [api] StorefrontConfigController:
       GET /api/storefront-config?domain={shopDomain}
5. StorefrontConfigController → StorefrontConfigService: getConfig(domain)
6. StorefrontConfigService → DeepMergeUtil: merge(masterTemplate, tenantOverrides)
   DeepMergeUtil → StorefrontConfigService: mergedConfig
7. StorefrontConfigService → RedisClient: set(cacheKey, mergedConfig, TTL=3600)
8. StorefrontConfigResolver → ComponentResolver: resolveComponent('ProductCard', config)
9. ComponentResolver → DynamicComponentRenderer: render(componentDef, productData)
10. StorefrontPage → Visitor: HTML (Server-rendered)
```

**[VIẾT VĂN XUÔI]** Giải thích hai nhánh Cache HIT/MISS. Tham chiếu `\ref{table:uc07}` và `\ref{fig:deep_merge_flow}` (khai báo trong Ch.5) để minh họa thuật toán Deep Merge. TTL = 3600 giây.

---

### §4.2.3 `\subsection{Thiết kế cơ sở dữ liệu}` — Độ dài 2–4 trang

#### E-R Diagram PostgreSQL: `fig:er_postgres`

**File ảnh:** `Hinhve/er_postgres.png`

**Các entity và quan hệ:**
```
TENANT (1) ──< (N) SHOP
TENANT (1) ──< (N) USER
SHOP   (1) ──< (N) PRODUCT
SHOP   (1) ──< (N) ORDER
ORDER  (1) ──< (N) ORDER_ITEM
PRODUCT (1) ──< (N) ORDER_ITEM
TEMPLATE (1) ──< (N) TENANT  [tenant được gán template khi đăng ký]
```

**Bảng TENANT:**
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR(255) | |
| slug | VARCHAR(100) UNIQUE | |
| plan | ENUM | FREE/PRO/ENTERPRISE |
| createdAt | TIMESTAMP | |

**Bảng SHOP:**
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | UUID PK | |
| tenantId | UUID FK → TENANT | |
| domain | VARCHAR(255) UNIQUE | custom domain |
| primaryColor | VARCHAR(7) | hex |
| logoUrl | TEXT | MinIO URL |
| templateId | UUID FK → TEMPLATE | |

**Bảng PRODUCT:**
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | UUID PK | |
| shopId | UUID FK → SHOP | |
| name | VARCHAR(255) | |
| price | DECIMAL(10,2) | |
| imageUrl | TEXT | MinIO URL |
| slug | VARCHAR(255) | |
| isActive | BOOLEAN | |

**Bảng ORDER:**
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | UUID PK | |
| shopId | UUID FK → SHOP | |
| customerId | UUID nullable | null = guest checkout |
| status | ENUM | PENDING/PAID/SHIPPED/CANCELLED |
| totalAmount | DECIMAL(10,2) | |
| paymentMethod | VARCHAR(50) | COD/STRIPE/MOMO |
| transactionId | VARCHAR(255) nullable | từ payment gateway |
| webhookVerified | BOOLEAN | kết quả HMAC-SHA256 |
| createdAt | TIMESTAMP | |

**Bảng ORDER_ITEM:**
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | UUID PK | |
| orderId | UUID FK → ORDER | |
| productId | UUID FK → PRODUCT | |
| quantity | INTEGER | |
| unitPrice | DECIMAL(10,2) | **snapshot giá tại thời điểm mua** |

---

#### Schema MongoDB: `fig:er_mongo`

**File ảnh:** `Hinhve/er_mongo.png`

**Collection `layouts`:**
```javascript
{
  _id: ObjectId,
  shopId: String,       // FK → PostgreSQL SHOP.id
  tenantId: String,
  pageType: String,     // "home"|"product"|"cart"|"checkout"
  version: Number,
  components: [{
    id: String,
    type: String,       // "HeroBanner"|"ProductGrid"|...
    order: Number,
    config: Object      // JSON tự do — Zero-file core
  }],
  updatedAt: Date
}
```

**Collection `component_registry`:**
```javascript
{
  _id: ObjectId,
  componentType: String,   // "HeroBanner"
  defaultConfig: Object,   // Master Template defaults
  schema: Object,          // JSON Schema validation
  version: String
}
```

**Collection `analytics_events`:**
```javascript
{
  _id: ObjectId,
  tenantId: String,
  shopId: String,
  eventType: String,   // "page_view"|"add_to_cart"|"purchase"
  sessionId: String,
  payload: Object,
  createdAt: Date
}
```

**[VIẾT VĂN XUÔI]** Giải thích lý do dùng MongoDB: cấu trúc JSON lồng nhau sâu, biến động theo tenant → không thể cố định với PostgreSQL schema. Redis cache collection `layouts` với **TTL 3600 giây**. Khi UC-03 chạy, `invalidateCache` xóa Redis key.

---

## 5. SECTION §4.3 — XÂY DỰNG ỨNG DỤNG

### §4.3.1 `\subsection{Thư viện và công cụ sử dụng}`

> ⚠️ **Đã sửa từ audit:** Thêm Tailwind CSS và Zod. Sửa Prisma từ 6.x → **5.x**.

**Bảng LaTeX đầy đủ (dùng `\resizebox`):**

```latex
\begin{table}[H]
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll}
\hline
\textbf{Mục đích} & \textbf{Công cụ / Thư viện} & \textbf{Địa chỉ URL} \\ \hline
Quản lý Monorepo    & Turborepo 2.x       & https://turbo.build/ \\ \hline
Backend Framework   & NestJS 11.x         & https://nestjs.com/ \\ \hline
Frontend Framework  & Next.js 15.x        & https://nextjs.org/ \\ \hline
ORM (PostgreSQL)    & Prisma 5.x          & https://www.prisma.io/ \\ \hline
ODM (MongoDB)       & Mongoose 8.x        & https://mongoosejs.com/ \\ \hline
Cache               & Redis 7.x (ioredis) & https://redis.io/ \\ \hline
Object Storage      & MinIO               & https://min.io/ \\ \hline
Xác thực            & Better Auth 1.x     & https://www.better-auth.com/ \\ \hline
Ngôn ngữ lập trình  & TypeScript 5.x      & https://www.typescriptlang.org/ \\ \hline
Runtime             & Node.js 20 LTS      & https://nodejs.org/ \\ \hline
Styling Framework   & Tailwind CSS 4.x    & https://tailwindcss.com/ \\ \hline
Schema Validation   & Zod 3.x             & https://zod.dev/ \\ \hline
Container hóa       & Docker 26.x         & https://www.docker.com/ \\ \hline
Điều phối container & Kubernetes 1.29+    & https://kubernetes.io/ \\ \hline
IDE                 & Visual Studio Code  & https://code.visualstudio.com/ \\ \hline
Kiểm thử            & Jest 29.x           & https://jestjs.io/ \\ \hline
API Testing         & Postman             & https://www.postman.com/ \\ \hline
Vẽ UML              & draw.io             & https://www.drawio.com/ \\ \hline
\end{tabular}%
}
\caption{Danh sách thư viện và công cụ sử dụng}
\label{table:tools}
\end{table}
```

**[VIẾT VĂN XUÔI sau bảng]** Nhắc lại rằng đây là các công nghệ đã được luận giải chi tiết trong Chương 3. Bảng `\ref{table:tools}` tổng hợp 18 công cụ theo mục đích sử dụng.

---

### §4.3.2 `\subsection{Kết quả đạt được}`

**[VIẾT VĂN XUÔI — Đoạn 1]** Mô tả 4 sản phẩm đóng gói: (i) `api` — NestJS REST API, Docker image, Kubernetes Deployment; (ii) `storefront` — Next.js storefront động; (iii) `dashboard` — Next.js quản lý tenant; (iv) `admin` — Next.js quản trị nền tảng. Thêm 5 shared packages quản lý nội bộ trong Turborepo.

**Bảng thống kê LOC:**

```latex
\begin{table}[H]
\centering
\begin{tabular}{llll}
\hline
\textbf{Thành phần} & \textbf{Số dòng mã nguồn} & \textbf{Số lớp/Module} & \textbf{Dung lượng} \\ \hline
api (NestJS)         & [ĐIỀN\_LOC\_API]   & [ĐIỀN\_MODULE\_API]  & [ĐIỀN\_SIZE\_API]   \\ \hline
storefront (Next.js) & [ĐIỀN\_LOC\_SF]    & [ĐIỀN\_COMP\_SF]     & [ĐIỀN\_SIZE\_SF]    \\ \hline
dashboard (Next.js)  & [ĐIỀN\_LOC\_DASH]  & [ĐIỀN\_COMP\_DASH]   & [ĐIỀN\_SIZE\_DASH]  \\ \hline
admin (Next.js)      & [ĐIỀN\_LOC\_ADM]   & [ĐIỀN\_COMP\_ADM]    & [ĐIỀN\_SIZE\_ADM]   \\ \hline
@repo/database       & [ĐIỀN\_LOC\_DB]    & [ĐIỀN\_SCHEMA]       & ---                 \\ \hline
@repo/utils          & [ĐIỀN\_LOC\_UTILS] & ---                  & ---                 \\ \hline
\textbf{Tổng cộng} & \textbf{[ĐIỀN\_LOC\_TOTAL]} & \textbf{[ĐIỀN\_TOTAL]} & \textbf{[ĐIỀN\_TOTAL\_SIZE]} \\ \hline
\end{tabular}
\caption{Thống kê mã nguồn hệ thống ShopVolo v2}
\label{table:stats}
\end{table}
```

> **Cách điền số liệu:** Chạy `npx cloc --by-file-by-lang apps/ packages/` trong thư mục gốc Turborepo.

---

### §4.3.3 `\subsection{Minh họa các chức năng chính}`

> ⚠️ **Đã sửa từ audit:** Tất cả placeholder dùng `Picture3.png`. **KHÔNG dùng `activity_*.png`** làm demo screenshot. Caption ghi rõ `(placeholder — thay bằng screenshot thực)`.

**5 chức năng, mỗi chức năng 1 hình + 1 đoạn văn mô tả:**

| STT | Chức năng | Label | Caption |
|---|---|---|---|
| 1 | Đăng ký và Onboarding tenant | `fig:demo_onboarding` | Màn hình Đăng ký và Khởi tạo Shop (UC-01) |
| 2 | Dashboard quản lý sản phẩm | `fig:demo_product` | Màn hình Dashboard quản lý sản phẩm (UC-04) |
| 3 | Upload ảnh + AI xóa nền | `fig:demo_ai_upload` | Màn hình Upload ảnh và kết quả xử lý AI |
| 4 | Thanh toán và đơn hàng | `fig:demo_checkout` | Màn hình Thanh toán và quản lý Đơn hàng (UC-09) |
| 5 | Storefront động | `fig:demo_storefront` | Màn hình Storefront động theo cấu hình tenant |

---

## 6. SECTION §4.4 — KIỂM THỬ — Độ dài 2–3 trang

**[VIẾT VĂN XUÔI — Mở đầu]** Giới thiệu 2 kỹ thuật kiểm thử: (i) black-box (Equivalence Partitioning + BVA) cho API endpoint và form; (ii) white-box (Statement Coverage) cho `DeepMergeUtil.merge()` và `OrderService.verifySignature()`.

### Bảng TC-01 — UC-01 Đăng ký Tenant

```latex
\begin{table}[H]
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{lllll}
\hline
\textbf{TC\#} & \textbf{Điều kiện đầu vào} & \textbf{Dữ liệu thử} & \textbf{Kết quả mong đợi} & \textbf{Kết quả thực tế} \\ \hline
TC-01-01 & Email, mật khẩu, tên shop hợp lệ & email=test@example.com, pwd=Test@1234, shop=MyShop & HTTP 201, JWT token, tenantId & [ĐIỀN] \\ \hline
TC-01-02 & Email đã tồn tại & email=existed@example.com & HTTP 409, code 9996 & [ĐIỀN] \\ \hline
TC-01-03 & Email sai định dạng & email=notanemail & HTTP 400, validation error & [ĐIỀN] \\ \hline
TC-01-04 & Mật khẩu dưới 8 ký tự & pwd=123 & HTTP 400, validation error & [ĐIỀN] \\ \hline
TC-01-05 & Tên shop chứa ký tự đặc biệt & shop=My@Shop! & HTTP 400, validation error & [ĐIỀN] \\ \hline
TC-01-06 & Đăng ký thành công, kiểm tra Master Template & (như TC-01-01) & Tenant.templateId không null trong DB & [ĐIỀN] \\ \hline
\end{tabular}%
}
\caption{Bảng kiểm thử UC-01 — Đăng ký Tenant}
\label{table:tc_uc01}
\end{table}
```

### Bảng TC-07 — UC-07 Duyệt sản phẩm động

> ⚠️ **Đã sửa từ audit:** Bảng có dữ liệu đầy đủ, không chỉ là comment.

```latex
\begin{table}[H]
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{lllll}
\hline
\textbf{TC\#} & \textbf{Điều kiện đầu vào} & \textbf{Dữ liệu thử} & \textbf{Kết quả mong đợi} & \textbf{Kết quả thực tế} \\ \hline
TC-07-01 & Domain hợp lệ, Redis cache MISS & domain=shop1.shopvolo.vn (lần đầu truy cập) & Gọi API, render đúng, Redis TTL=3600s được set & [ĐIỀN] \\ \hline
TC-07-02 & Domain hợp lệ, Redis cache HIT & domain=shop1.shopvolo.vn (lần 2, trong 1h) & Không gọi API, render từ cache, thời gian dưới 10ms & [ĐIỀN] \\ \hline
TC-07-03 & Domain không tồn tại trong hệ thống & domain=fake-shop-xyz.shopvolo.vn & HTTP 404, trang lỗi hiển thị & [ĐIỀN] \\ \hline
TC-07-04 & Tenant có override màu sắc & domain=shop1, primaryColor=\#FF0000 trong config & Storefront render màu \#FF0000, không phải màu Master Template & [ĐIỀN] \\ \hline
TC-07-05 & Tenant chưa có override, mới đăng ký & domain=shop2 (chưa tùy chỉnh) & Storefront render màu mặc định của Master Template & [ĐIỀN] \\ \hline
\end{tabular}%
}
\caption{Bảng kiểm thử UC-07 — Duyệt sản phẩm động}
\label{table:tc_uc07}
\end{table}
```

### Tổng kết kiểm thử

**[VIẾT VĂN XUÔI]**
```
Tổng số test case thiết kế: [ĐIỀN_TC_TOTAL]
Số test case đạt (Pass):     [ĐIỀN_TC_PASS]
Số test case không đạt:      [ĐIỀN_TC_FAIL]
Tỷ lệ đạt:                  [ĐIỀN_%]%
```
Nếu có test fail → phân tích nguyên nhân trong 1–2 câu. Nhắc người đọc rằng test case chi tiết cho các chức năng còn lại nằm trong Phụ lục B.

---

## 7. SECTION §4.5 — TRIỂN KHAI

> ⚠️ **Đã sửa từ audit:** Cấu hình server viết thành văn xuôi, không dùng code block.

**[VIẾT VĂN XUÔI — 3 đoạn]**

**Đoạn 1 — Mô hình triển khai Kubernetes:**
Mô tả kiến trúc triển khai: (i) Kubernetes Cluster với 3+ worker nodes; (ii) Nginx Ingress Controller định tuyến theo subdomain; (iii) PostgreSQL và MongoDB dưới dạng StatefulSet với PVC; (iv) Redis Deployment; (v) MinIO StatefulSet. Mỗi trong 4 app đóng thành Docker image riêng.

**Đoạn 2 — Cấu hình phần cứng (theo kế hoạch — viết thành văn xuôi):**
Ví dụ: *"Control Plane Node được cấu hình với 2 vCPU và 4 GB RAM. Mỗi Worker Node trong cụm ba máy được trang bị 4 vCPU, 8 GB RAM và ổ SSD 50 GB. Database Node được tách riêng với 8 vCPU, 16 GB RAM và ổ SSD 200 GB nhằm đảm bảo hiệu năng I/O. Giới hạn bộ nhớ: NestJS 1024 MB, PostgreSQL và MongoDB mỗi thành phần 512 MB, Redis 256 MB theo yêu cầu tại `\ref{section:2.4}`."*

**Đoạn 3 — Kết quả triển khai hiện tại:**
Hệ thống đang chạy trên Docker Compose cục bộ với đầy đủ dịch vụ phụ thuộc. Triển khai Kubernetes sẽ thực hiện giai đoạn tiếp theo.

---

## 8. PHỤ LỤC A — CÁC LỚP BỔ SUNG

**File:** `Chuong/Phu_luc_A.tex`

> ⚠️ **Quan trọng:** Thêm nội dung vào **CUỐI** file `Phu_luc_A.tex`, SAU tất cả các `\section` hiện có (các section về quy định chung của trường). KHÔNG thêm vào giữa file.

**Nội dung thêm vào cuối:**
```latex
\section{Thiết kế chi tiết các lớp bổ sung}
\label{section:appendix_classes}

Phần này trình bày thiết kế chi tiết các lớp không nằm trong bốn lớp chủ đạo được
trình bày tại phần \ref{subsection:4.2.2}.

\subsection{AuthService}
% Class: AuthService | Package: api/src/auth/ (dùng @repo/auth)
% Attributes: betterAuth: BetterAuthClient, prisma: PrismaClient
% Methods: validateSession(token): Promise<Session|null>
%          getCurrentUser(sessionId): Promise<User>
%          revokeSession(sessionId): Promise<void>
% [Vẽ class diagram, lưu Hinhve/class_auth.png]

\subsection{ProductService}
% Class: ProductService | Package: api/src/product/
% Attributes: prisma: PrismaClient, minioService: MinioService, aiService: AIBackgroundRemovalService
% Methods: createProduct, updateProduct, deleteProduct, uploadImage, enqueueAIJob
% [Vẽ class diagram, lưu Hinhve/class_product.png]

\subsection{DeepMergeUtil}
% Class: DeepMergeUtil | Package: @repo/utils
% Methods: merge<T>(base: T, override: Partial<T>): T
%   Thuật toán đệ quy: với mỗi key trong override,
%   nếu cả hai bên là object → đệ quy merge,
%   ngược lại → override thắng (giữ nguyên keys không bị override trong base)
% [Vẽ class diagram, lưu Hinhve/class_deepmerge.png]

\subsection{ComponentResolver}
% Class: ComponentResolver | Package: storefront/src/lib/
% Attributes: registry: Map<string, ComponentDefinition>
% Methods: resolve(type: string, config: object): React.ComponentType
%          register(type: string, definition: ComponentDefinition): void
% [Vẽ class diagram, lưu Hinhve/class_resolver.png]
```

---

## 9. HÌNH ẢNH CẦN VẼ — CHECKLIST

Tất cả hình sau cần được vẽ bằng **draw.io** (hoặc PlantUML), export PNG, lưu vào thư mục `Hinhve/`:

| File cần tạo | Nội dung | Section |
|---|---|---|
| `pkg_overview.png` | Package diagram 3 tầng tổng quan | §4.1.2 |
| `pkg_detail_core.png` | Packages lõi với 6 quan hệ UML | §4.1.3 |
| `pkg_detail_apps.png` | Apps với quan hệ nội bộ | §4.1.3 |
| `class_tenant.png` | Class diagram TenantService | §4.2.2 |
| `class_storefront.png` | Class diagram StorefrontConfigResolver | §4.2.2 |
| `class_order.png` | Class diagram OrderService | §4.2.2 |
| `class_middleware.png` | Class diagram TenantMiddleware | §4.2.2 |
| `seq_uc01.png` | Sequence diagram UC-01 Onboarding | §4.2.2 |
| `seq_uc04.png` | Sequence diagram UC-04 Product+AI | §4.2.2 |
| `seq_uc07.png` | Sequence diagram UC-07 Dynamic Render | §4.2.2 |
| `er_postgres.png` | E-R diagram PostgreSQL | §4.2.3 |
| `er_mongo.png` | MongoDB collections schema | §4.2.3 |
| `class_auth.png` | Class diagram AuthService (Phụ lục A) | Phụ lục A |
| `class_product.png` | Class diagram ProductService (Phụ lục A) | Phụ lục A |

**Placeholder tạm thời:** Trong khi chờ vẽ, dùng `Hinhve/Picture1.png` hoặc `Picture2.png` với caption ghi rõ `(placeholder — thay bằng Hinhve/tên_file.png)`.

---

## 10. CHECKLIST TRƯỚC KHI NỘP

- [ ] Đã xóa toàn bộ văn bản hướng dẫn gốc của giảng viên khỏi `.tex`
- [ ] Đã xóa hình `fig:Fig1` và `fig:Fig2` (ví dụ của giảng viên) khỏi `.tex`
- [ ] Mọi `\label{}` đã được `\ref{}` ít nhất 1 lần trong văn bản
- [ ] Labels dùng dấu `_` không dùng dấu `-` (ví dụ: `fig:activity_onboarding`)
- [ ] `fig:deep_merge_flow` chỉ dùng `\ref{}` trong Ch.4, KHÔNG khai báo `\label{}`
- [ ] Không có bullet/gạch đầu dòng trong văn bản LaTeX
- [ ] TTL Redis là **3600 giây** ở mọi nơi đề cập
- [ ] §4.2.2 có đúng **4 lớp**: TenantService, StorefrontConfigResolver, OrderService, TenantMiddleware
- [ ] AuthService đã chuyển sang Phụ lục A
- [ ] Seq. UC-04: `createProduct` trong DB trước, AI job là bất đồng bộ sau
- [ ] Bảng TC-07 có đầy đủ 5 dòng dữ liệu thực (không chỉ comment)
- [ ] Bảng công cụ có Tailwind CSS 4.x, Zod 3.x, Prisma **5.x** (không phải 6.x)
- [ ] Placeholder hình UI dùng `Picture3.png`, KHÔNG dùng `activity_*.png`
- [ ] Phụ lục A được thêm vào CUỐI `Phu_luc_A.tex`
- [ ] Cấu hình server trong §4.5 viết thành đoạn văn (không dùng code block)
- [ ] Tất cả hình cần vẽ đã được tạo và thay thế placeholder
