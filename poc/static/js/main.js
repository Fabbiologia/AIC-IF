// Main JavaScript file for AIC-IF Framework

// Add smooth scrolling to all links
document.addEventListener('DOMContentLoaded', function() {
    const smoothScrollLinks = document.querySelectorAll('a.smooth-scroll');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Render citation contribution score bars
    const contributionBars = document.querySelectorAll('.contribution-bar');
    contributionBars.forEach(bar => {
        const score = parseFloat(bar.getAttribute('data-score'));
        const fill = bar.querySelector('.contribution-fill');
        if (fill) {
            fill.style.width = `${score * 100}%`;
            
            // Color based on score
            if (score >= 0.8) {
                fill.style.backgroundColor = '#28a745'; // green
            } else if (score >= 0.5) {
                fill.style.backgroundColor = '#ffc107'; // yellow
            } else {
                fill.style.backgroundColor = '#dc3545'; // red
            }
        }
    });

    // Format dates
    const dateElements = document.querySelectorAll('.format-date');
    dateElements.forEach(element => {
        const dateString = element.textContent.trim();
        try {
            const date = new Date(dateString);
            element.textContent = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
        } catch (e) {
            console.error('Error formatting date:', e);
        }
    });

    // Citation tracker form submission handling
    const citationForm = document.getElementById('citation-form');
    if (citationForm) {
        citationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = {
                doi: document.getElementById('doi').value,
                source_title: document.getElementById('source_title').value,
                source_type: document.getElementById('source_type').value,
                authors: document.getElementById('authors').value,
                ai_model: document.getElementById('ai_model').value,
                context: document.getElementById('context').value,
                contribution_score: parseFloat(document.getElementById('contribution_score').value)
            };
            
            // Send to API
            fetch('/api/citations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Show success message
                    const alertContainer = document.getElementById('alert-container');
                    alertContainer.innerHTML = `
                        <div class="alert alert-success alert-dismissible fade show" role="alert">
                            Citation logged successfully!
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `;
                    
                    // Refresh recent citations list
                    fetchRecentCitations();
                    
                    // Reset form
                    citationForm.reset();
                }
            })
            .catch(error => {
                console.error('Error logging citation:', error);
                // Show error message
                const alertContainer = document.getElementById('alert-container');
                alertContainer.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Error logging citation. Please try again.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;
            });
        });
    }

    // Function to fetch recent citations
    function fetchRecentCitations() {
        const recentCitationsContainer = document.getElementById('recent-citations');
        if (recentCitationsContainer) {
            fetch('/api/citations?limit=10')
                .then(response => response.json())
                .then(data => {
                    if (data.citations && data.citations.length > 0) {
                        const citationItems = data.citations.map(citation => {
                            // Determine contribution class
                            let contributionClass = 'low-contribution';
                            if (citation.contribution_score >= 0.8) {
                                contributionClass = 'high-contribution';
                            } else if (citation.contribution_score >= 0.5) {
                                contributionClass = 'medium-contribution';
                            }
                            
                            return `
                                <div class="citation-item fade-in">
                                    <h5>${citation.source_title || 'Unknown title'}</h5>
                                    <p class="mb-1">${citation.authors || 'Unknown author'} - <span class="text-muted">${citation.source_type || 'journal'}</span></p>
                                    <p class="mb-2 text-muted small">DOI: ${citation.doi}</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span class="text-muted small">Cited by ${citation.ai_model}</span>
                                        <span class="contribution-score ${contributionClass}">
                                            Score: ${citation.contribution_score.toFixed(2)}
                                        </span>
                                    </div>
                                </div>
                            `;
                        }).join('');
                        
                        recentCitationsContainer.innerHTML = citationItems;
                    } else {
                        recentCitationsContainer.innerHTML = '<p class="text-center text-muted">No citation events yet</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching recent citations:', error);
                    recentCitationsContainer.innerHTML = '<p class="text-center text-danger">Error loading citations</p>';
                });
        }
    }

    // Call the function to load recent citations on page load
    if (document.getElementById('recent-citations')) {
        fetchRecentCitations();
    }

    // Dashboard stats loader
    const dashboardStats = document.getElementById('dashboard-stats');
    if (dashboardStats) {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-citations').textContent = data.total_citations || 0;
                document.getElementById('unique-sources').textContent = data.unique_sources || 0;
                document.getElementById('unique-models').textContent = data.unique_models || 0;
                document.getElementById('unique-researchers').textContent = data.unique_researchers || 0;
            })
            .catch(error => {
                console.error('Error fetching dashboard stats:', error);
            });
    }

    // Top cited works loader
    const topCitedContainer = document.getElementById('top-cited');
    if (topCitedContainer) {
        fetch('/api/stats/top-cited')
            .then(response => response.json())
            .then(data => {
                if (data.citations && data.citations.length > 0) {
                    const citationItems = data.citations.map(citation => {
                        return `
                            <div class="citation-item fade-in">
                                <h5>${citation.title}</h5>
                                <p class="mb-1">${citation.authors} - <span class="text-muted">${citation.type}</span></p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="text-muted small">DOI: ${citation.doi}</span>
                                    <span class="badge bg-primary">${citation.citation_count} citations</span>
                                </div>
                                <div class="mt-2">
                                    <small class="text-muted">AIC-IF Score: ${citation.aicif_score.toFixed(2)}</small>
                                    <div class="contribution-bar">
                                        <div class="contribution-fill" style="width: ${citation.aicif_score * 100}%"></div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('');
                    
                    topCitedContainer.innerHTML = citationItems;
                } else {
                    topCitedContainer.innerHTML = '<p class="text-center text-muted">No citation data available</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching top cited works:', error);
                topCitedContainer.innerHTML = '<p class="text-center text-danger">Error loading top cited works</p>';
            });
    }

    // Model interpretation demo functionality
    const analyzeContributionsForm = document.getElementById('analyze-form');
    if (analyzeContributionsForm) {
        analyzeContributionsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            document.getElementById('loading-indicator').classList.remove('d-none');
            document.getElementById('results-container').classList.add('d-none');
            
            // Collect form data
            const formData = {
                dataset_id: document.getElementById('dataset').value,
                model_id: document.getElementById('model').value,
                method: document.querySelector('input[name="method"]:checked').value
            };
            
            // Send to API
            fetch('/demo/feature-contributions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading state
                document.getElementById('loading-indicator').classList.add('d-none');
                document.getElementById('results-container').classList.remove('d-none');
                
                // Display results
                renderContributionChart(data.contributions);
            })
            .catch(error => {
                console.error('Error analyzing contributions:', error);
                document.getElementById('loading-indicator').classList.add('d-none');
                document.getElementById('error-message').classList.remove('d-none');
            });
        });
    }

    // Function to render contribution chart using Chart.js
    function renderContributionChart(contributions) {
        if (!contributions || contributions.length === 0) return;
        
        const chartContainer = document.getElementById('contribution-chart');
        if (!chartContainer) return;
        
        // Format data for chart
        const labels = contributions.map(c => c.feature);
        const values = contributions.map(c => c.value);
        const colors = contributions.map(c => {
            const value = c.value;
            if (value >= 0.8) return 'rgba(40, 167, 69, 0.7)';
            if (value >= 0.5) return 'rgba(255, 193, 7, 0.7)';
            return 'rgba(220, 53, 69, 0.7)';
        });
        
        // Create chart
        const ctx = chartContainer.getContext('2d');
        
        // Clear previous chart if exists
        if (window.contributionChart) {
            window.contributionChart.destroy();
        }
        
        window.contributionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feature Contribution',
                    data: values,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.7', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Contribution Value'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Feature'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Feature Contribution Analysis'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                return `Contribution: ${(value * 100).toFixed(1)}%`;
                            }
                        }
                    }
                }
            }
        });
        
        // Also populate the table
        const tableBody = document.getElementById('contribution-table-body');
        if (tableBody) {
            tableBody.innerHTML = contributions.map(contribution => {
                return `
                    <tr>
                        <td>${contribution.feature}</td>
                        <td>${(contribution.value * 100).toFixed(1)}%</td>
                        <td>${contribution.doi}</td>
                    </tr>
                `;
            }).join('');
        }
    }
});
