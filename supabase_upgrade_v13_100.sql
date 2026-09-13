-- David 戰情室 V13：60檔 -> 100檔 升級
-- 在既有 Supabase 專案 SQL Editor 執行一次。

do $$
begin
  if exists (
    select 1 from pg_constraint
    where conrelid = 'public.stock_config'::regclass
      and contype = 'c'
      and pg_get_constraintdef(oid) like '%position%between 1 and 60%'
  ) then
    execute (
      select 'alter table public.stock_config drop constraint ' || quote_ident(conname)
      from pg_constraint
      where conrelid = 'public.stock_config'::regclass
        and contype = 'c'
        and pg_get_constraintdef(oid) like '%position%between 1 and 60%'
      limit 1
    );
  end if;
end $$;

alter table public.stock_config
  drop constraint if exists stock_config_position_check;

alter table public.stock_config
  add constraint stock_config_position_check check (position between 1 and 100);

-- 驗證：應顯示 1..100 可用，不會刪除 stock_history。
