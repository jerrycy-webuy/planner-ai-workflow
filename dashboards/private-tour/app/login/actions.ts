'use server';

import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';
import { ALLOWED_EMAIL_DOMAIN } from '@/lib/supabase/config';

export async function sendMagicLink(formData: FormData) {
  const email = String(formData.get('email') ?? '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+$/.test(email) || !email.endsWith(ALLOWED_EMAIL_DOMAIN)) {
    redirect('/login?error=domain');
  }

  const origin = process.env.NEXT_PUBLIC_SITE_URL || headers().get('origin') || '';
  const { error } = await createClient().auth.signInWithOtp({
    email,
    options: { emailRedirectTo: `${origin}/auth/callback` },
  });
  redirect(error ? '/login?error=send' : '/login?sent=1');
}
