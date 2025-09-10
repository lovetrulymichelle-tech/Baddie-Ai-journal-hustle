"""Flask application for the Baddie AI Journal dashboard."""

from flask import Flask, render_template, jsonify, request, make_response
from datetime import datetime, timedelta
import json

from .models import create_database_engine, create_tables, get_session_maker, JournalEntryDB, JournalEntry, InsightData
from .insights import InsightsHelper, create_sample_data


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Default configuration
    app.config.update({
        'SECRET_KEY': 'dev-secret-key-change-in-production',
        'DATABASE_URL': 'sqlite:///journal.db',
        'DEBUG': True
    })
    
    if config:
        app.config.update(config)
    
    # Initialize database
    engine = create_database_engine(app.config['DATABASE_URL'])
    create_tables(engine)
    SessionMaker = get_session_maker(engine)
    
    @app.route('/')
    def dashboard():
        """Main dashboard view."""
        return render_template('dashboard.html')
    
    @app.route('/api/insights')
    def api_insights():
        """API endpoint for insights data."""
        try:
            # For now, use sample data. In production, load from database
            insight_data = create_sample_data()
            helper = InsightsHelper(insight_data)
            
            # Calculate all insights
            insights = {
                'streak': helper.calculate_streak(),
                'daily_counts': helper.get_daily_counts(30),
                'mood_breakdown': helper.get_mood_breakdown(),
                'category_breakdown': helper.get_category_breakdown(),
                'top_tags': helper.get_top_tags(10),
                'metrics': helper.get_totals_and_metrics(),
                'mood_trends': helper.get_mood_trends(30)
            }
            
            return jsonify(insights)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/export/csv')
    def export_csv():
        """Export insights as CSV."""
        try:
            export_type = request.args.get('type', 'entries')
            insight_data = create_sample_data()
            helper = InsightsHelper(insight_data)
            
            if export_type == 'summary':
                csv_data = helper.export_insights_summary_csv()
                filename = f'insights_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            else:
                csv_data = helper.export_to_csv()
                filename = f'journal_entries_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            response = make_response(csv_data)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '0.1.0'
        })
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)