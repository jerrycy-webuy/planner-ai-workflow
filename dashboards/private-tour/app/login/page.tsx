import { redirect } from 'next/navigation';
import { supabaseConfig, ALLOWED_EMAIL_DOMAIN } from '@/lib/supabase/config';
import { sendMagicLink } from './actions';

export const dynamic = 'force-dynamic';

const ERRORS: Record<string, string> = {
  domain: `请使用公司邮箱(${ALLOWED_EMAIL_DOMAIN})。`,
  send: '登录邮件发送失败,请稍后重试。',
  link: '登录链接已失效,请重新获取。',
};

export default function LoginPage({ searchParams }: { searchParams: Record<string, string | undefined> }) {
  if (!supabaseConfig()) redirect('/'); // 示例数据模式不需要登录

  const error = searchParams.error ? ERRORS[searchParams.error] : undefined;
  return (
    <main className="login">
      <form action={sendMagicLink} className="login-card">
        <h1>Private Tour 数据看板</h1>
        <p className="muted">输入公司邮箱,我们会发一封登录链接给你。</p>
        <label htmlFor="email">邮箱</label>
        <input id="email" name="email" type="email" required placeholder={`name${ALLOWED_EMAIL_DOMAIN}`} autoComplete="email" />
        <button type="submit" className="btn btn-primary">发送登录链接</button>
        {searchParams.sent && <p className="note-ok">已发送,请到邮箱点击链接登录。</p>}
        {error && <p className="note-err">{error}</p>}
        <p className="muted small">能看哪些市场由数据平台白名单决定;没权限请联系数据平台负责人。</p>
      </form>
    </main>
  );
}
