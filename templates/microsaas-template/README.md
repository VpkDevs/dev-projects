# MicroSaaS Template

A production-ready MicroSaaS template built with Next.js 14, TypeScript, Prisma, and Stripe.

## Features

- 🚀 **Next.js 14** with App Router
- 💎 **TypeScript** for type safety
- 🎨 **Tailwind CSS** for styling
- 🔐 **NextAuth.js** for authentication
- 💳 **Stripe** integration for payments
- 🗄️ **Prisma** ORM with PostgreSQL
- 📊 **React Query** for data fetching
- 🎭 **Framer Motion** for animations
- 🔥 **React Hot Toast** for notifications
- 📈 **Analytics** ready (GA, PostHog)
- 🐛 **Error tracking** with Sentry

## Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   ```
   Fill in your environment variables in `.env.local`

3. **Set up the database:**
   ```bash
   npx prisma generate
   npx prisma db push
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open [http://localhost:3000](http://localhost:3000)**

## Project Structure

```
├── src/
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/             # Utility functions and configurations
│   └── styles/          # Global styles
├── prisma/
│   └── schema.prisma    # Database schema
├── public/              # Static assets
└── tests/              # Test files
```

## Key Technologies

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** Next.js API Routes, Prisma
- **Database:** PostgreSQL (can be switched to MySQL/SQLite)
- **Authentication:** NextAuth.js
- **Payments:** Stripe
- **State Management:** React Query
- **Testing:** Jest, React Testing Library
- **Deployment:** Vercel (recommended)

## Deployment

1. **Deploy to Vercel:**
   - Push your code to GitHub
   - Import project to Vercel
   - Add environment variables
   - Deploy

2. **Database hosting:**
   - Use Supabase, Neon, or PlanetScale for PostgreSQL
   - Update DATABASE_URL in production

## Customization

- Modify `src/app/page.tsx` for the landing page
- Update `prisma/schema.prisma` for your data model
- Customize styles in `tailwind.config.ts`
- Add API routes in `src/app/api/`

## License

MIT
