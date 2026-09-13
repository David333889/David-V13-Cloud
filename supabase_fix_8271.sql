-- V13.100 PATCH1：修正宇瞻 8271 市場別
-- 官方 TWSE：8271 宇瞻為上市公司，Yahoo ticker = 8271.TW

update public.stock_config
set market = 'TW', updated_at = now()
where code = '8271';

-- 若先前曾寫入錯誤市場別的歷史資料，一併修正欄位；沒有資料也不會有影響。
update public.stock_history
set market = 'TW', symbol = '8271.TW', updated_at = now()
where code = '8271';
