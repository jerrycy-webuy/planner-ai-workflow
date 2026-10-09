/** 两个公开变量都配了才连库;否则整站走示例数据,也不要求登录 */
export function supabaseConfig(): { url: string; anonKey: string } | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  return url && anonKey ? { url, anonKey } : null;
}

/** 看板用户邮箱域名。只做登录页的提前拦截,真正的权限在 reporting.dashboard_viewers 白名单 */
export const ALLOWED_EMAIL_DOMAIN = '@webuy.global';
