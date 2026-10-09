import { NextResponse, type NextRequest } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { supabaseConfig } from '@/lib/supabase/config';

export async function POST(request: NextRequest) {
  if (supabaseConfig()) await createClient().auth.signOut();
  return NextResponse.redirect(`${request.nextUrl.origin}/login`, { status: 303 });
}
