# MongoDB Database Analysis

**Analysis Date:** 2025-11-15 20:21:11

**Week Start:** 2025-11-10

---

## Summary

- **Databases with updates:** 2
- **Collections with updates:** 8

---

## Database: `bills`

### Collection: `consumers`

- **Total Documents:** 39
- **Updated This Week:** 9

#### Schema Fields

| Field | Type |
|-------|------|
| `address` | str |
| `company_name` | str |
| `created_at` | datetime |
| `created_by` | str |
| `email` | NoneType |
| `first_name` | str |
| `italian_tax_code` | str |
| `last_name` | str |
| `phone` | str |
| `town` | str |
| `updated_at` | datetime |
| `updated_by` | str |
| `user_id` | ObjectId (reference) |
| `zip_code` | str |

#### Indexes


---

### Collection: `file_processing_jobs`

- **Total Documents:** 161
- **Updated This Week:** 32

#### Schema Fields

| Field | Type |
|-------|------|
| `bill_id` | NoneType |
| `callback_url` | NoneType |
| `completed_at` | datetime |
| `consumer_id` | str |
| `created_at` | datetime |
| `created_by` | str |
| `current_stage` | str |
| `errors` | list |
| `final_path` | NoneType |
| `hints` | NoneType |
| `job_id` | str |
| `max_retries` | int |
| `original_filename` | str |
| `result_data.billing.annual_consumption.by_bands.f1` | NoneType |
| `result_data.billing.annual_consumption.by_bands.f1_percentage` | NoneType |
| `result_data.billing.annual_consumption.by_bands.f2` | NoneType |
| `result_data.billing.annual_consumption.by_bands.f2_percentage` | NoneType |
| `result_data.billing.annual_consumption.by_bands.f3` | NoneType |
| `result_data.billing.annual_consumption.by_bands.f3_percentage` | NoneType |
| `result_data.billing.annual_consumption.by_bands.from_date` | NoneType |
| `result_data.billing.annual_consumption.by_bands.to_date` | NoneType |
| `result_data.billing.annual_consumption.cost.from_date` | str |
| `result_data.billing.annual_consumption.cost.previous_year_annual_cost` | float |
| `result_data.billing.annual_consumption.cost.to_date` | str |
| `result_data.billing.annual_consumption.total` | int |
| `result_data.billing.current_bill_consumption.f1` | int |
| `result_data.billing.current_bill_consumption.f2` | int |
| `result_data.billing.current_bill_consumption.f3` | int |
| `result_data.billing.current_bill_consumption.from_date` | str |
| `result_data.billing.current_bill_consumption.to_date` | str |
| `result_data.billing.current_bill_consumption.total_amount` | float |
| `result_data.billing.current_bill_consumption.total_consumption` | int |
| `result_data.billing.invoice_date` | str |
| `result_data.billing.invoice_number` | str |
| `result_data.billing.issue_date` | str |
| `result_data.billing.payment_method` | str |
| `result_data.billing.payment_status` | str |
| `result_data.contract.activation_date` | str |
| `result_data.contract.billing_cycle` | str |
| `result_data.contract.contract_expiration_date` | NoneType |
| `result_data.contract.offer.offer_code` | str |
| `result_data.contract.offer.offer_name` | str |
| `result_data.contract.offer.offer_type` | str |
| `result_data.contract.tariff_expiration_date` | NoneType |
| `result_data.cost_components[].fixed.components` | list |
| `result_data.cost_components[].fixed.discounts` | list |
| `result_data.cost_components[].fixed.dispatching` | list |
| `result_data.cost_components[].from_date` | str |
| `result_data.cost_components[].to_date` | str |
| `result_data.cost_components[].usage_based.capacity_market_fee` | list |
| `result_data.cost_components[].usage_based.components[].band` | NoneType |
| `result_data.cost_components[].usage_based.components[].name` | str |
| `result_data.cost_components[].usage_based.components[].unit_price` | float |
| `result_data.cost_components[].usage_based.dispatching` | list |
| `result_data.customer.address` | str |
| `result_data.customer.codice_destinatario` | NoneType |
| `result_data.customer.company_name` | NoneType |
| `result_data.customer.customer_type` | str |
| `result_data.customer.email` | NoneType |
| `result_data.customer.first_name` | NoneType |
| `result_data.customer.italian_tax_code` | str |
| `result_data.customer.last_name` | NoneType |
| `result_data.customer.name` | str |
| `result_data.customer.pec` | NoneType |
| `result_data.customer.phone` | NoneType |
| `result_data.customer.surname` | str |
| `result_data.customer.town` | str |
| `result_data.customer.zip_code` | str |
| `result_data.service_provider.available_power` | float |
| `result_data.service_provider.contracted_power` | float |
| `result_data.service_provider.market_type` | str |
| `result_data.service_provider.name` | str |
| `result_data.service_provider.pod` | str |
| `result_data.service_provider.renewable_energy_only` | bool |
| `result_data.service_provider.service_address` | str |
| `result_data.service_provider.service_town` | str |
| `result_data.service_provider.service_zip_code` | str |
| `result_data.service_provider.supply_code` | str |
| `result_data.service_provider.supply_type` | str |
| `result_data.service_provider.tariff_type` | str |
| `result_data.service_provider.voltage` | str |
| `retry_count` | int |
| `service_account_id` | str |
| `staging_path` | str |
| `status` | str |
| `storage_document_id` | str |
| `updated_at` | datetime |
| `user_id` | str |

#### Indexes


---

### Collection: `files`

- **Total Documents:** 183
- **Updated This Week:** 32

#### Schema Fields

| Field | Type |
|-------|------|
| `__v` | int |
| `created_at` | datetime |
| `filename` | str |
| `mime_type` | str |
| `path` | str |
| `provider` | str |
| `updated_at` | datetime |
| `user` | str |

#### Indexes


---

### Collection: `service_accounts`

- **Total Documents:** 59
- **Updated This Week:** 12

#### Schema Fields

| Field | Type |
|-------|------|
| `available_power` | float |
| `consumer_id` | ObjectId (reference) |
| `contract.activation_date` | datetime |
| `contract.billing_cycle` | str |
| `contract.contract_expiration_date` | NoneType |
| `contract.offer.offer_code` | str |
| `contract.offer.offer_name` | str |
| `contract.offer.offer_type` | str |
| `contract.tariff_expiration_date` | datetime |
| `contracted_power` | float |
| `created_at` | datetime |
| `created_by` | str |
| `market_type` | str |
| `pod` | str |
| `renewable_energy_only` | bool |
| `service_address` | str |
| `service_town` | str |
| `service_zip_code` | str |
| `status` | str |
| `supply_code` | str |
| `supply_type` | str |
| `tariff_type` | str |
| `updated_at` | datetime |
| `updated_by` | str |
| `vendor_id` | ObjectId (reference) |
| `voltage` | str |

#### Indexes


---

### Collection: `users`

- **Total Documents:** 52
- **Updated This Week:** 20

#### Schema Fields

| Field | Type |
|-------|------|
| `codice_destinatario` | NoneType |
| `company.address` | str |
| `company.company_name` | str |
| `company.tax_id` | str |
| `company.town` | str |
| `company.zip_code` | str |
| `consent_accepted` | bool |
| `created_at` | datetime |
| `created_by` | str |
| `customer_type` | str |
| `email` | NoneType |
| `mandato_id` | NoneType |
| `pec` | NoneType |
| `personal.first_name` | str |
| `personal.id_card` | NoneType |
| `personal.last_name` | str |
| `personal.tax_id` | str |
| `phone` | str |
| `stripe_id` | NoneType |
| `updated_at` | datetime |
| `updated_by` | str |

#### Indexes


---

### Collection: `utility_bills`

- **Total Documents:** 73
- **Updated This Week:** 18

#### Schema Fields

| Field | Type |
|-------|------|
| `billing.annual_consumption.by_bands.f1` | int |
| `billing.annual_consumption.by_bands.f1_percentage` | float |
| `billing.annual_consumption.by_bands.f2` | int |
| `billing.annual_consumption.by_bands.f2_percentage` | float |
| `billing.annual_consumption.by_bands.f3` | int |
| `billing.annual_consumption.by_bands.f3_percentage` | float |
| `billing.annual_consumption.by_bands.from_date` | NoneType |
| `billing.annual_consumption.by_bands.to_date` | NoneType |
| `billing.annual_consumption.cost.from_date` | datetime |
| `billing.annual_consumption.cost.previous_year_annual_cost` | float |
| `billing.annual_consumption.cost.to_date` | datetime |
| `billing.annual_consumption.total` | int |
| `billing.current_bill_consumption.f1` | int |
| `billing.current_bill_consumption.f2` | int |
| `billing.current_bill_consumption.f3` | int |
| `billing.current_bill_consumption.from_date` | datetime |
| `billing.current_bill_consumption.to_date` | datetime |
| `billing.current_bill_consumption.total_amount` | float |
| `billing.current_bill_consumption.total_consumption` | int |
| `billing.invoice_date` | datetime |
| `billing.invoice_number` | str |
| `billing.issue_date` | datetime |
| `billing.payment_method` | str |
| `billing.payment_status` | str |
| `consumer_id` | ObjectId (reference) |
| `contract.activation_date` | datetime |
| `contract.billing_cycle` | str |
| `contract.contract_expiration_date` | NoneType |
| `contract.offer.code` | str |
| `contract.offer.name` | str |
| `contract.offer.type` | str |
| `contract.tariff_expiration_date` | datetime |
| `cost_components` | list |
| `created_at` | datetime |
| `created_by` | str |
| `is_archived` | bool |
| `original_filename` | str |
| `service_account_id` | ObjectId (reference) |
| `source` | str |
| `status` | str |
| `storage_document_id` | str |
| `supply.address` | str |
| `supply.available_power` | float |
| `supply.code` | str |
| `supply.contracted_power` | float |
| `supply.customer_type` | str |
| `supply.market_type` | str |
| `supply.pod` | str |
| `supply.renewable_only` | bool |
| `supply.tariff_type` | str |
| `supply.town` | str |
| `supply.vendor_piva` | NoneType |
| `supply.voltage` | str |
| `supply.zip_code` | str |
| `type` | str |
| `updated_at` | datetime |
| `updated_by` | str |
| `user_display_name` | str |
| `user_id` | ObjectId (reference) |
| `vendor_id` | ObjectId (reference) |
| `vendor_name` | str |

#### Indexes


---

### Collection: `whitelist_entries`

- **Total Documents:** 18
- **Updated This Week:** 16

#### Schema Fields

| Field | Type |
|-------|------|
| `allowed_products` | list |
| `created_at` | datetime |
| `created_by` | str |
| `deleted` | bool |
| `deleted_at` | NoneType |
| `deleted_by` | NoneType |
| `kind` | str |
| `metadata.environment` | str |
| `metadata.source` | str |
| `name` | str |
| `notes` | str |
| `rate_limits.messages_per_day` | int |
| `rate_limits.messages_per_hour` | int |
| `rate_limits.messages_per_minute` | int |
| `status` | str |
| `tenant` | str |
| `updated_at` | datetime |
| `updated_by` | str |
| `user_id` | str |
| `valid_from` | NoneType |
| `valid_to` | NoneType |
| `value` | str |

#### Indexes

- **user_idx**: `tenant` (1), `user_id` (1)
- **validity_idx**: `valid_from` (1), `valid_to` (1)
- **audit_idx**: `created_at` (-1)
- **lookup_idx**: `tenant` (1), `kind` (1), `value` (1), `status` (1)

---

## Database: `companion_agent`

### Collection: `phone_thread_mappings`

- **Total Documents:** 15
- **Updated This Week:** 12

#### Schema Fields

| Field | Type |
|-------|------|
| `created_at` | datetime |
| `phone_number` | str |
| `thread_id` | str |
| `updated_at` | datetime |

#### Indexes

- **phone_number_1**: `phone_number` (1)
- **thread_id_1**: `thread_id` (1)

---

## Recommendations for MCP Server

### High Priority Collections

- **`bills.file_processing_jobs`**: 32 updates this week - High activity
- **`bills.files`**: 32 updates this week - High activity
- **`bills.service_accounts`**: 12 updates this week - High activity
- **`bills.users`**: 20 updates this week - High activity
- **`bills.utility_bills`**: 18 updates this week - High activity
- **`bills.whitelist_entries`**: 16 updates this week - High activity
- **`companion_agent.phone_thread_mappings`**: 12 updates this week - High activity

### Suggested MCP Tools

Based on the collections analyzed, consider creating MCP tools for:

#### 1. Utility Bills Tools (High Priority)

**Query Tools:**
- `get_bills_by_date_range(start_date, end_date)` - Get bills in date range
- `get_bills_by_vendor(vendor_name)` - Filter by vendor
- `get_bills_by_creator(created_by)` - Filter by creator email
- `get_bills_by_status(status)` - Filter by status (published, draft, archived)
- `get_bills_by_type(type)` - Filter by type (ELECTRICITY, GAS, etc.)

**Aggregation Tools:**
- `sum_bill_amounts(filters)` - Total bill amounts with optional filters
- `sum_annual_kwh(filters)` - Total annual kWh consumption
- `sum_annual_costs(filters)` - Total annual energy costs
- `count_bills_by_vendor(date_range)` - Count bills grouped by vendor
- `count_bills_by_creator(date_range)` - Count bills grouped by creator
- `average_bill_amount(filters)` - Average bill amount
- `average_annual_cost_per_bill(filters)` - Average annual cost per bill

-**Comparison Tools:**
- `compare_periods(period1_start, period1_end, period2_start, period2_end)` - Compare two periods
- `compare_day_vs_previous_day()` - Yesterday vs previous day
- `compare_week_vs_last_week()` - This week vs last week
- `compare_by_vendor(vendor_name, period1, period2)` - Vendor comparison

**Pre-computed Queries:**
- `get_today_stats()` - Today's bills statistics
- `get_this_week_stats()` - This week's statistics
- `get_this_month_stats()` - This month's statistics
- `get_top_vendors(limit=10, date_range)` - Top N vendors by bill count
- `get_top_creators(limit=10, date_range)` - Top N creators by bill count
- `get_active_bills()` - Non-archived bills with status=published

#### 2. File Processing Jobs Tools

**Query Tools:**
- `get_jobs_by_status(status)` - Filter by status (pending, processing, completed, failed)
- `get_jobs_by_stage(current_stage)` - Filter by processing stage
- `get_failed_jobs(date_range)` - Get failed jobs with errors
- `get_jobs_by_user(user_id)` - Get jobs for specific user

**Aggregation Tools:**
- `count_jobs_by_status()` - Count jobs grouped by status
- `count_jobs_by_stage()` - Count jobs grouped by stage
- `get_processing_times()` - Average processing times
- `get_error_summary()` - Summary of errors

#### 3. Users & Consumers Tools

**Query Tools:**
- `get_users_by_type(customer_type)` - Filter by customer type
- `search_users_by_name(name)` - Search by name
- `get_users_by_company(company_name)` - Filter by company
- `get_consumers_by_user(user_id)` - Get consumers for a user

**Aggregation Tools:**
- `count_users_by_type()` - Count users by customer type
- `count_consumers_by_user()` - Count consumers per user

#### 4. Service Accounts Tools

**Query Tools:**
- `get_service_accounts_by_vendor(vendor_id)` - Filter by vendor
- `get_service_accounts_by_status(status)` - Filter by status
- `get_service_accounts_by_consumer(consumer_id)` - Filter by consumer
- `get_active_service_accounts()` - Active service accounts

**Aggregation Tools:**
- `sum_contracted_power(filters)` - Total contracted power
- `count_by_vendor()` - Count service accounts by vendor
- `count_by_market_type()` - Count by market type (FREE_MARKET, etc.)

#### 5. Files Tools

**Query Tools:**
- `get_files_by_user(user)` - Get files for a user
- `get_files_by_provider(provider)` - Filter by storage provider
- `get_recent_files(limit=50)` - Get recently uploaded files

**Aggregation Tools:**
- `count_files_by_provider()` - Count files by storage provider
- `count_files_by_user()` - Count files per user

#### 6. Whitelist Entries Tools

**Query Tools:**
- `get_whitelist_by_kind(kind)` - Filter by kind
- `get_active_whitelist_entries()` - Non-deleted entries
- `get_whitelist_by_user(user_id)` - Get entries for a user
- `get_whitelist_by_tenant(tenant)` - Filter by tenant

### Recommended Pre-made Queries for MCP Server

Based on the analysis, these queries should be pre-made for quick access:

1. **Daily Bills Summary**: Today's bills count, total amount, total kWh, total cost
2. **Weekly Bills Summary**: This week's bills with comparison to last week
3. **Top 5 Vendors This Week**: Most active vendors by bill count
4. **Top 5 Creators This Week**: Most active creators by bill count
5. **Processing Jobs Status**: Count of jobs by status (pending, processing, completed, failed)
6. **Active Service Accounts**: Count of active service accounts by vendor
7. **Recent File Uploads**: Last 10 files uploaded
8. **User Activity**: Users with most bills this week

### Data Relationships to Leverage

- `utility_bills` → `user_id` → `users`
- `utility_bills` → `consumer_id` → `consumers`
- `utility_bills` → `service_account_id` → `service_accounts`
- `utility_bills` → `vendor_id` → `vendors` (in vendors database)
- `file_processing_jobs` → `storage_document_id` → `files`
- `service_accounts` → `consumer_id` → `consumers`
- `consumers` → `user_id` → `users`

### Common Filter Patterns

1. **Date-based**: `created_at >= start_date AND created_at <= end_date`
2. **Status-based**: `status = 'published' AND is_archived = false`
3. **User-based**: `created_by = 'email@domain.com' OR created_by NOT IN excluded_users`
4. **Vendor-based**: `vendor_name = 'Vendor Name'`
5. **Type-based**: `type = 'ELECTRICITY' OR type = 'GAS'`

