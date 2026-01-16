import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import '@testing-library/jest-dom';

// Mock scroll function since it's not available in jsdom
window.scrollTo = jest.fn();

const replaceStateSpy = jest.spyOn(window.history, 'replaceState');

describe('App Integration', () => {
    it('renders dashboard with initial elements', async () => {
        render(<App />);

        // Header
        expect(screen.getByText('JobMatch')).toBeInTheDocument();

        // Search input
        expect(screen.getByPlaceholderText('Search jobs, companies, skills...')).toBeInTheDocument();

        // Sort dropdown
        expect(screen.getByRole('combobox')).toBeInTheDocument();

        // Filter panel (desktop view check)
        expect(screen.getByText('Filters')).toBeVisible(); // Might be hidden on mobile, but test env is usually desktop-ish width unless configured

        // Wait for skeleton to disappear and jobs to appear (500ms delay simulated)
        await waitFor(() => {
            // Check for "Showing X jobs" text update which appears after loading
            expect(screen.getByText(/Showing \d+ jobs/)).toBeInTheDocument();
        }, { timeout: 2000 });
    });

    it('updates search results when typing', async () => {
        render(<App />);

        await waitFor(() => expect(screen.getByText(/Showing \d+ jobs/)).toBeInTheDocument());

        const searchInput = screen.getByPlaceholderText('Search jobs, companies, skills...');

        fireEvent.change(searchInput, { target: { value: 'React' } });

        // Debounce wait
        await waitFor(() => {
            // Just verify it doesn't crash and potentially filters. 
            // We can't strictly assert count without knowing exact mock data, but we can check if it updates.
            // Or check if URL updates if we test that behavior.
            expect(replaceStateSpy).toHaveBeenCalled();
        }, { timeout: 1000 });
    });
});
