import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { supabaseConfig } from './config';

export function createClient() {
  const cfg = supabaseConfig();
  if (!cfg) throw new Error('Supabase is not configured');
  const cookieStore = cookies();

  return createServerClient(cfg.url, cfg.anonKey, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
        } catch {
          // Server Component 里不能写 cookie;会话刷新由 middleware 负责
        }
      },
    },
  });
}
