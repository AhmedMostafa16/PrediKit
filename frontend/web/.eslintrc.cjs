module.exports = {
  extends: [
    'mantine',
    'plugin:prettier/recommended',
    'plugin:react/recommended',
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parserOptions: {
    parser: '@typescript-eslint/parser',
    extraFileExtensions: ['.json'],
    project: './tsconfig.json',
  },
  rules: {
    'react/react-in-jsx-scope': 'off',
    camelcase: 'error',
    'spaced-comment': 'error',
    quotes: ['error', 'single'],
    'no-duplicate-imports': 'error',
    'no-console': 'warn',
    '@typescript-eslint/no-explicit-any': 'off',
  },
  plugins: ['react', 'prettier', 'react-hooks', '@typescript-eslint'],
};
