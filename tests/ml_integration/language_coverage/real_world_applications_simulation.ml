// Real-World Applications Simulation Test
// Demonstrates practical ML programming patterns through realistic application scenarios

import string;
import datetime;
import regex;
import collections;

// Utility functions for safe array operations
function safe_upsert(arr, pos, item) {
    if (pos < arr.length) {
        // Update existing position
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            if (i == pos) {
                new_arr = collections.append(new_arr, item);
            } else {
                new_arr = collections.append(new_arr, arr[i]);
            }
            i = i + 1;
        }
        return new_arr;
    } else {
        // Append to end
        return collections.append(arr, item);
    }
}

function safe_append(arr, item) {
    return collections.append(arr, item);
}

// Utility function to safely convert values to strings
function to_string(value) {
    if (typeof(value) == "string") {
        return value;
    } elif (typeof(value) == "number") {
        return value + "";
    } elif (typeof(value) == "boolean") {
        return value ? "true" : "false";
    } else {
        return "[object]";
    }
}

// Math utilities
function math_ceil(x) {
    if (x == math_int(x)) {
        return x;
    } else {
        return math_int(x) + 1;
    }
}

function math_int(x) {
    if (x >= 0) {
        return x - (x % 1);
    } else {
        return x - (x % 1);
    }
}

function math_min(a, b) {
    return a < b ? a : b;
}

// E-commerce order processing system simulation
function ecommerce_order_processing() {
    print("=== E-commerce Order Processing System ===");

    // Product catalog
    function create_product_catalog() {
        products = [];
        safe_append(products, {id: "LAPTOP001", name: "Gaming Laptop", price: 1299.99, category: "Electronics", stock: 15});
        safe_append(products, {id: "PHONE002", name: "Smartphone", price: 799.00, category: "Electronics", stock: 25});
        safe_append(products, {id: "BOOK003", name: "Programming Book", price: 49.95, category: "Books", stock: 100});
        safe_append(products, {id: "HEADSET004", name: "Wireless Headset", price: 199.99, category: "Electronics", stock: 30});
        safe_append(products, {id: "TABLET005", name: "Tablet Device", price: 449.00, category: "Electronics", stock: 20});
        return products;
    }

    function find_product_by_id(catalog, product_id) {
        i = 0;
        while (i < catalog.length) {
            if (catalog[i].id == product_id) {
                return catalog[i];
            }
            i = i + 1;
        }
        return null;
    }

    function calculate_order_total(items) {
        subtotal = 0;
        tax_rate = 0.08;

        i = 0;
        while (i < items.length) {
            item = items[i];
            item_total = item.price * item.quantity;
            subtotal = subtotal + item_total;
            i = i + 1;
        }

        tax_amount = subtotal * tax_rate;
        shipping = subtotal > 100 ? 0 : 9.99;
        total = subtotal + tax_amount + shipping;

        return {
            subtotal: subtotal,
            tax: tax_amount,
            shipping: shipping,
            total: total
        };
    }

    function validate_order(order, catalog) {
        errors = [];

        // Validate customer information
        if (order.customer.email == null || !regex.test("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", order.customer.email)) {
            safe_append(errors, "Invalid email address");
        }

        if (order.customer.name == null || string.length(order.customer.name) < 2) {
            safe_append(errors, "Customer name is required");
        }

        // Validate order items
        if (order.items == null || order.items.length == 0) {
            safe_append(errors, "Order must contain at least one item");
        } else {
            j = 0;
            while (j < order.items.length) {
                item = order.items[j];
                product = find_product_by_id(catalog, item.product_id);

                if (product == null) {
                    safe_append(errors, "Product " + item.product_id + " not found");
                } elif (item.quantity <= 0) {
                    safe_append(errors, "Invalid quantity for " + item.product_id);
                } elif (product != null && item.quantity > product.stock) {
                    safe_append(errors, "Insufficient stock for " + product.name);
                }

                j = j + 1;
            }
        }

        return {
            valid: errors.length == 0,
            errors: errors
        };
    }

    function process_order(order, catalog) {
        validation = validate_order(order, catalog);

        if (!validation.valid) {
            return {
                success: false,
                order_id: null,
                errors: validation.errors,
                total: 0
            };
        }

        // Build order items with product details
        processed_items = [];
        k = 0;
        while (k < order.items.length) {
            item = order.items[k];
            product = find_product_by_id(catalog, item.product_id);

            processed_item = {
                product_id: item.product_id,
                name: product.name,
                price: product.price,
                quantity: item.quantity,
                total: product.price * item.quantity
            };

            safe_append(processed_items, processed_item);
            k = k + 1;
        }

        // Calculate totals
        order_total = calculate_order_total(processed_items);

        // Generate order ID
        order_id = "ORD" + to_string(datetime.timestamp()) + "_" + string.substring(order.customer.email, 0, 3);

        return {
            success: true,
            order_id: order_id,
            customer: order.customer,
            items: processed_items,
            totals: order_total,
            created_at: datetime.now(),
            status: "confirmed"
        };
    }

    // Test the e-commerce system
    catalog = create_product_catalog();
    print("Created product catalog with " + to_string(catalog.length) + " products");

    // Test orders
    valid_order = {
        customer: {
            name: "John Doe",
            email: "john.doe@example.com",
            phone: "555-123-4567"
        },
        items: []
    };
    safe_append(valid_order.items, {product_id: "LAPTOP001", quantity: 1});
    safe_append(valid_order.items, {product_id: "HEADSET004", quantity: 2});

    invalid_order = {
        customer: {
            name: "Jane",
            email: "invalid-email",
            phone: "123"
        },
        items: []
    };
    safe_append(invalid_order.items, {product_id: "NONEXISTENT", quantity: 1});
    safe_append(invalid_order.items, {product_id: "LAPTOP001", quantity: 100});

    print("");
    print("Processing valid order:");
    valid_result = process_order(valid_order, catalog);
    if (valid_result.success) {
        print("  Order ID: " + valid_result.order_id);
        print("  Total: $" + to_string(valid_result.totals.total));
        print("  Items: " + to_string(valid_result.items.length));
    }

    print("");
    print("Processing invalid order:");
    invalid_result = process_order(invalid_order, catalog);
    if (!invalid_result.success) {
        print("  Validation failed with " + to_string(invalid_result.errors.length) + " errors:");
        l = 0;
        while (l < invalid_result.errors.length) {
            print("    - " + invalid_result.errors[l]);
            l = l + 1;
        }
    }

    return {
        system: "ecommerce",
        valid_order_processed: valid_result.success,
        invalid_order_rejected: !invalid_result.success,
        catalog_size: catalog.length
    };
}

// Blog content management system simulation
function blog_content_management() {
    print("");
    print("=== Blog Content Management System ===");

    // Blog post structure and operations
    function create_blog_post(title, content, author, tags) {
        post_id = "POST_" + to_string(datetime.timestamp());
        slug = generate_slug(title);
        word_count = count_words(content);
        reading_time = math_ceil(word_count / 200); // Assuming 200 words per minute

        return {
            id: post_id,
            title: title,
            slug: slug,
            content: content,
            author: author,
            tags: tags,
            word_count: word_count,
            reading_time: reading_time,
            created_at: datetime.now(),
            published: false,
            views: 0,
            comments: []
        };
    }

    function generate_slug(title) {
        // Convert to lowercase and replace spaces with hyphens
        slug = string.lower(title);
        slug = string.replace_all(slug, " ", "-");
        slug = regex.replace_all(slug, "[^a-z0-9\\-]", "");
        // Remove multiple consecutive hyphens
        while (string.contains(slug, "--")) {
            slug = string.replace_all(slug, "--", "-");
        }
        return slug;
    }

    function count_words(content) {
        if (string.length(content) == 0) {
            return 0;
        }
        words = string.split(content, " ");
        return words.length;
    }

    function publish_post(post) {
        if (string.length(post.title) < 5) {
            return {success: false, error: "Title too short"};
        }

        if (post.word_count < 50) {
            return {success: false, error: "Content too short"};
        }

        post.published = true;
        post.published_at = datetime.now();

        return {success: true, message: "Post published successfully"};
    }

    function add_comment(post, author, content) {
        if (string.length(content) < 10) {
            return {success: false, error: "Comment too short"};
        }

        comment = {
            id: "COMMENT_" + to_string(datetime.timestamp()),
            author: author,
            content: content,
            created_at: datetime.now(),
            approved: false
        };

        safe_append(post.comments, comment);
        return {success: true, comment_id: comment.id};
    }

    function search_posts(posts, query) {
        results = [];
        query_lower = string.lower(query);

        i = 0;
        while (i < posts.length) {
            post = posts[i];

            // Search in title and content
            title_match = string.contains(string.lower(post.title), query_lower);
            content_match = string.contains(string.lower(post.content), query_lower);
            tag_match = false;

            // Search in tags
            j = 0;
            while (j < post.tags.length) {
                if (string.contains(string.lower(post.tags[j]), query_lower)) {
                    tag_match = true;
                    break;
                }
                j = j + 1;
            }

            if (title_match || content_match || tag_match) {
                safe_append(results, {
                    post: post,
                    match_type: title_match ? "title" : (content_match ? "content" : "tags")
                });
            }

            i = i + 1;
        }

        return results;
    }

    function generate_analytics(posts) {
        total_posts = posts.length;
        published_posts = 0;
        total_views = 0;
        total_comments = 0;
        total_words = 0;

        tag_frequency = {};
        author_stats = {};

        k = 0;
        while (k < posts.length) {
            post = posts[k];

            if (post.published) {
                published_posts = published_posts + 1;
            }

            total_views = total_views + post.views;
            total_comments = total_comments + post.comments.length;
            total_words = total_words + post.word_count;

            // Count tags
            l = 0;
            while (l < post.tags.length) {
                tag = post.tags[l];
                if (tag_frequency[tag] == null) {
                    tag_frequency[tag] = 0;
                }
                tag_frequency[tag] = tag_frequency[tag] + 1;
                l = l + 1;
            }

            // Count authors
            author = post.author;
            if (author_stats[author] == null) {
                author_stats[author] = {posts: 0, words: 0};
            }
            author_stats[author].posts = author_stats[author].posts + 1;
            author_stats[author].words = author_stats[author].words + post.word_count;

            k = k + 1;
        }

        return {
            total_posts: total_posts,
            published_posts: published_posts,
            draft_posts: total_posts - published_posts,
            total_views: total_views,
            total_comments: total_comments,
            total_words: total_words,
            avg_words_per_post: total_posts > 0 ? total_words / total_posts : 0,
            tag_frequency: tag_frequency,
            author_stats: author_stats
        };
    }

    // Test the blog system
    print("Testing blog content management system:");

    // Create sample blog posts
    posts = [];

    post1_tags = [];
    safe_append(post1_tags, "programming");
    safe_append(post1_tags, "ml");
    safe_append(post1_tags, "tutorial");
    safe_append(post1_tags, "beginners");

    post1 = create_blog_post(
        "Getting Started with ML Programming",
        "ML is a powerful programming language that combines functional programming concepts with modern syntax. In this comprehensive guide, we'll explore the fundamental concepts of ML programming, including variable declarations, function definitions, and control structures. Whether you're new to programming or coming from other languages, this tutorial will provide you with the foundation you need to start building applications in ML.",
        "Alice Developer",
        post1_tags
    );

    post2_tags = [];
    safe_append(post2_tags, "data-structures");
    safe_append(post2_tags, "algorithms");
    safe_append(post2_tags, "advanced");
    safe_append(post2_tags, "performance");

    post2 = create_blog_post(
        "Advanced Data Structures in ML",
        "Data structures are the building blocks of efficient algorithms. In this advanced tutorial, we'll dive deep into implementing complex data structures like binary search trees, hash tables, and graphs using ML. We'll also cover performance considerations and best practices for choosing the right data structure for your specific use case.",
        "Bob Programmer",
        post2_tags
    );

    post3_tags = [];
    safe_append(post3_tags, "short");

    post3 = create_blog_post(
        "Short Post",
        "Too short content.",
        "Charlie Writer",
        post3_tags
    );

    safe_append(posts, post1);
    safe_append(posts, post2);
    safe_append(posts, post3);

    print("Created " + to_string(posts.length) + " blog posts");

    // Publish posts
    publish_result1 = publish_post(post1);
    publish_result2 = publish_post(post2);
    publish_result3 = publish_post(post3);

    print("Publishing results:");
    print("  Post 1: " + (publish_result1.success ? "Published" : publish_result1.error));
    print("  Post 2: " + (publish_result2.success ? "Published" : publish_result2.error));
    print("  Post 3: " + (publish_result3.success ? "Published" : publish_result3.error));

    // Add comments
    add_comment(post1, "Reader1", "Great tutorial! Very helpful for beginners.");
    add_comment(post1, "Reader2", "Clear explanations and good examples.");
    add_comment(post2, "Expert", "Excellent deep dive into data structures.");

    // Simulate some views
    post1.views = 1250;
    post2.views = 890;
    post3.views = 45;

    // Search functionality
    search_results = search_posts(posts, "data");
    print("");
    print("Search results for 'data':");
    print("  Found " + to_string(search_results.length) + " matching posts");

    // Generate analytics
    analytics = generate_analytics(posts);
    print("");
    print("Blog Analytics:");
    print("  Total posts: " + to_string(analytics.total_posts));
    print("  Published posts: " + to_string(analytics.published_posts));
    print("  Total views: " + to_string(analytics.total_views));
    print("  Total comments: " + to_string(analytics.total_comments));
    print("  Average words per post: " + to_string(math_int(analytics.avg_words_per_post)));

    return {
        system: "blog_cms",
        posts_created: posts.length,
        posts_published: analytics.published_posts,
        total_views: analytics.total_views,
        search_results: search_results.length
    };
}

// Task management and project tracking system
function task_management_system() {
    print("");
    print("=== Task Management and Project Tracking System ===");

    // Task and project structures
    function create_project(name, description, deadline) {
        return {
            id: "PROJ_" + to_string(datetime.timestamp()),
            name: name,
            description: description,
            deadline: deadline,
            created_at: datetime.now(),
            status: "active",
            tasks: [],
            team_members: [],
            progress: 0
        };
    }

    function create_task(title, description, priority, estimated_hours) {
        return {
            id: "TASK_" + to_string(datetime.timestamp()),
            title: title,
            description: description,
            priority: priority, // "high", "medium", "low"
            estimated_hours: estimated_hours,
            actual_hours: 0,
            status: "todo", // "todo", "in_progress", "completed"
            assigned_to: null,
            created_at: datetime.now(),
            completed_at: null,
            dependencies: [],
            comments: []
        };
    }

    function add_task_to_project(project, task) {
        task.project_id = project.id;
        safe_append(project.tasks, task);
        update_project_progress(project);
    }

    function assign_task(task, assignee) {
        task.assigned_to = assignee;
        task.status = "in_progress";
        task.started_at = datetime.now();

        return {
            success: true,
            message: "Task assigned to " + assignee
        };
    }

    function complete_task(task) {
        if (task.status != "in_progress") {
            return {
                success: false,
                error: "Task must be in progress to complete"
            };
        }

        task.status = "completed";
        task.completed_at = datetime.now();

        return {
            success: true,
            message: "Task completed successfully"
        };
    }

    function update_project_progress(project) {
        if (project.tasks.length == 0) {
            project.progress = 0;
            return;
        }

        completed_tasks = 0;
        m = 0;
        while (m < project.tasks.length) {
            if (project.tasks[m].status == "completed") {
                completed_tasks = completed_tasks + 1;
            }
            m = m + 1;
        }

        project.progress = (completed_tasks / project.tasks.length) * 100;
    }

    function generate_project_report(project) {
        total_tasks = project.tasks.length;
        completed_tasks = 0;
        in_progress_tasks = 0;
        todo_tasks = 0;

        total_estimated = 0;
        total_actual = 0;

        priority_breakdown = {high: 0, medium: 0, low: 0};
        assignee_workload = {};

        n = 0;
        while (n < project.tasks.length) {
            task = project.tasks[n];

            if (task.status == "completed") {
                completed_tasks = completed_tasks + 1;
            } elif (task.status == "in_progress") {
                in_progress_tasks = in_progress_tasks + 1;
            } else {
                todo_tasks = todo_tasks + 1;
            }

            total_estimated = total_estimated + task.estimated_hours;
            total_actual = total_actual + task.actual_hours;

            priority_breakdown[task.priority] = priority_breakdown[task.priority] + 1;

            if (task.assigned_to != null) {
                if (assignee_workload[task.assigned_to] == null) {
                    assignee_workload[task.assigned_to] = {tasks: 0, hours: 0};
                }
                assignee_workload[task.assigned_to].tasks = assignee_workload[task.assigned_to].tasks + 1;
                assignee_workload[task.assigned_to].hours = assignee_workload[task.assigned_to].hours + task.estimated_hours;
            }

            n = n + 1;
        }

        // Calculate days until deadline
        days_until_deadline = datetime.days_between(datetime.now(), project.deadline);

        return {
            project_name: project.name,
            total_tasks: total_tasks,
            completed_tasks: completed_tasks,
            in_progress_tasks: in_progress_tasks,
            todo_tasks: todo_tasks,
            progress_percentage: project.progress,
            total_estimated_hours: total_estimated,
            total_actual_hours: total_actual,
            priority_breakdown: priority_breakdown,
            assignee_workload: assignee_workload,
            days_until_deadline: days_until_deadline,
            on_track: project.progress >= 50 || days_until_deadline > 30
        };
    }

    function find_overdue_tasks(projects) {
        overdue_tasks = [];
        current_date = datetime.now();

        o = 0;
        while (o < projects.length) {
            project = projects[o];

            if (datetime.compare(current_date, project.deadline) > 0 && project.progress < 100) {
                p = 0;
                while (p < project.tasks.length) {
                    task = project.tasks[p];

                    if (task.status != "completed") {
                        overdue_task_info = {
                            project_name: project.name,
                            task_title: task.title,
                            priority: task.priority,
                            assigned_to: task.assigned_to,
                            days_overdue: datetime.days_between(project.deadline, current_date)
                        };

                        safe_append(overdue_tasks, overdue_task_info);
                    }

                    p = p + 1;
                }
            }

            o = o + 1;
        }

        return overdue_tasks;
    }

    // Test the task management system
    print("Testing task management system:");

    // Create project
    project_deadline = datetime.add_days(datetime.now(), 60);
    web_project = create_project(
        "E-commerce Website Redesign",
        "Complete redesign of the company e-commerce website with modern UI/UX",
        project_deadline
    );

    print("Created project: " + web_project.name);

    // Create tasks
    tasks = [];
    safe_append(tasks, create_task("Design wireframes", "Create wireframes for all main pages", "high", 16));
    safe_append(tasks, create_task("Setup development environment", "Configure dev environment and CI/CD", "high", 8));
    safe_append(tasks, create_task("Implement user authentication", "Build login/register functionality", "high", 24));
    safe_append(tasks, create_task("Create product catalog", "Build product listing and search", "medium", 32));
    safe_append(tasks, create_task("Implement shopping cart", "Add cart functionality and checkout", "high", 20));
    safe_append(tasks, create_task("Payment integration", "Integrate with payment gateway", "high", 16));
    safe_append(tasks, create_task("Mobile responsive design", "Ensure mobile compatibility", "medium", 12));
    safe_append(tasks, create_task("Performance optimization", "Optimize loading times", "low", 8));
    safe_append(tasks, create_task("User testing", "Conduct usability testing", "medium", 16));
    safe_append(tasks, create_task("Documentation", "Write technical documentation", "low", 6));

    // Add tasks to project
    q = 0;
    while (q < tasks.length) {
        add_task_to_project(web_project, tasks[q]);
        q = q + 1;
    }

    print("Added " + to_string(tasks.length) + " tasks to project");

    // Assign and complete some tasks
    assign_task(tasks[0], "Alice Designer");
    assign_task(tasks[1], "Bob DevOps");
    assign_task(tasks[2], "Charlie Developer");

    complete_task(tasks[0]);
    complete_task(tasks[1]);

    // Update actual hours for completed tasks
    tasks[0].actual_hours = 18;
    tasks[1].actual_hours = 6;

    // Generate project report
    report = generate_project_report(web_project);

    print("");
    print("Project Report:");
    print("  Total tasks: " + to_string(report.total_tasks));
    print("  Completed: " + to_string(report.completed_tasks));
    print("  In progress: " + to_string(report.in_progress_tasks));
    print("  Todo: " + to_string(report.todo_tasks));
    print("  Progress: " + to_string(math_int(report.progress_percentage)) + "%");
    print("  Estimated hours: " + to_string(report.total_estimated_hours));
    print("  Days until deadline: " + to_string(report.days_until_deadline));
    print("  On track: " + to_string(report.on_track));

    // Test overdue detection (create a past-due project for testing)
    old_deadline = datetime.subtract_days(datetime.now(), 5);
    overdue_project = create_project("Legacy Migration", "Migrate legacy system", old_deadline);
    overdue_task = create_task("Migration task", "Complete migration", "high", 40);
    add_task_to_project(overdue_project, overdue_task);

    all_projects = [];
    safe_append(all_projects, web_project);
    safe_append(all_projects, overdue_project);

    overdue_tasks = find_overdue_tasks(all_projects);

    print("");
    print("Overdue tasks found: " + to_string(overdue_tasks.length));

    return {
        system: "task_management",
        project_created: true,
        tasks_added: tasks.length,
        progress_percentage: report.progress_percentage,
        overdue_tasks: overdue_tasks.length
    };
}

// Financial portfolio tracking system
function financial_portfolio_tracker() {
    print("");
    print("=== Financial Portfolio Tracking System ===");

    function create_portfolio(owner_name) {
        return {
            id: "PORTFOLIO_" + to_string(datetime.timestamp()),
            owner: owner_name,
            created_at: datetime.now(),
            holdings: [],
            transactions: [],
            total_value: 0,
            total_cost: 0,
            total_gain_loss: 0
        };
    }

    function add_holding(portfolio, symbol, quantity, purchase_price, current_price) {
        holding = {
            symbol: symbol,
            quantity: quantity,
            purchase_price: purchase_price,
            current_price: current_price,
            total_cost: quantity * purchase_price,
            current_value: quantity * current_price,
            gain_loss: (current_price - purchase_price) * quantity,
            gain_loss_percentage: ((current_price - purchase_price) / purchase_price) * 100
        };

        safe_append(portfolio.holdings, holding);

        // Add transaction record
        transaction = {
            id: "TXN_" + to_string(datetime.timestamp()),
            type: "buy",
            symbol: symbol,
            quantity: quantity,
            price: purchase_price,
            total: quantity * purchase_price,
            date: datetime.now()
        };

        safe_append(portfolio.transactions, transaction);

        update_portfolio_totals(portfolio);
        return holding;
    }

    function update_portfolio_totals(portfolio) {
        total_value = 0;
        total_cost = 0;

        r = 0;
        while (r < portfolio.holdings.length) {
            holding = portfolio.holdings[r];
            total_value = total_value + holding.current_value;
            total_cost = total_cost + holding.total_cost;
            r = r + 1;
        }

        portfolio.total_value = total_value;
        portfolio.total_cost = total_cost;
        portfolio.total_gain_loss = total_value - total_cost;
    }

    function update_market_prices(portfolio, price_updates) {
        // price_updates should be an object with symbol: new_price pairs
        s = 0;
        while (s < portfolio.holdings.length) {
            holding = portfolio.holdings[s];
            new_price = price_updates[holding.symbol];

            if (new_price != null) {
                holding.current_price = new_price;
                holding.current_value = holding.quantity * new_price;
                holding.gain_loss = (new_price - holding.purchase_price) * holding.quantity;
                holding.gain_loss_percentage = ((new_price - holding.purchase_price) / holding.purchase_price) * 100;
            }

            s = s + 1;
        }

        update_portfolio_totals(portfolio);
    }

    function generate_portfolio_analysis(portfolio) {
        if (portfolio.holdings.length == 0) {
            return {
                total_holdings: 0,
                message: "No holdings in portfolio"
            };
        }

        winners = [];
        losers = [];
        total_dividend_yield = 0;

        largest_holding = portfolio.holdings[0];
        largest_gain = portfolio.holdings[0];
        largest_loss = portfolio.holdings[0];

        t = 0;
        while (t < portfolio.holdings.length) {
            holding = portfolio.holdings[t];

            // Track winners and losers
            if (holding.gain_loss > 0) {
                safe_append(winners, holding);
            } else {
                safe_append(losers, holding);
            }

            // Find largest positions
            if (holding.current_value > largest_holding.current_value) {
                largest_holding = holding;
            }

            if (holding.gain_loss > largest_gain.gain_loss) {
                largest_gain = holding;
            }

            if (holding.gain_loss < largest_loss.gain_loss) {
                largest_loss = holding;
            }

            t = t + 1;
        }

        return {
            total_holdings: portfolio.holdings.length,
            total_value: portfolio.total_value,
            total_cost: portfolio.total_cost,
            total_gain_loss: portfolio.total_gain_loss,
            total_return_percentage: (portfolio.total_gain_loss / portfolio.total_cost) * 100,
            winners: winners.length,
            losers: losers.length,
            largest_holding: {
                symbol: largest_holding.symbol,
                value: largest_holding.current_value
            },
            best_performer: {
                symbol: largest_gain.symbol,
                gain: largest_gain.gain_loss,
                percentage: largest_gain.gain_loss_percentage
            },
            worst_performer: {
                symbol: largest_loss.symbol,
                loss: largest_loss.gain_loss,
                percentage: largest_loss.gain_loss_percentage
            }
        };
    }

    function calculate_diversification_score(portfolio) {
        if (portfolio.holdings.length <= 1) {
            return 0;
        }

        // Simple diversification score based on number of holdings
        // and distribution of values
        holding_count_score = math_min(portfolio.holdings.length * 10, 50);

        // Calculate value distribution score
        largest_position = 0;
        u = 0;
        while (u < portfolio.holdings.length) {
            position_percentage = (portfolio.holdings[u].current_value / portfolio.total_value) * 100;
            if (position_percentage > largest_position) {
                largest_position = position_percentage;
            }
            u = u + 1;
        }

        concentration_penalty = largest_position > 25 ? 20 : 0;
        distribution_score = 50 - concentration_penalty;

        return holding_count_score + distribution_score;
    }

    // Test the portfolio system
    print("Testing financial portfolio tracker:");

    // Create portfolio
    my_portfolio = create_portfolio("Investment Tracker User");
    print("Created portfolio for: " + my_portfolio.owner);

    // Add holdings
    add_holding(my_portfolio, "AAPL", 10, 150.00, 175.50);
    add_holding(my_portfolio, "GOOGL", 5, 2500.00, 2650.00);
    add_holding(my_portfolio, "MSFT", 8, 300.00, 285.00);
    add_holding(my_portfolio, "TSLA", 3, 800.00, 950.00);
    add_holding(my_portfolio, "AMZN", 2, 3200.00, 3100.00);

    print("Added " + to_string(my_portfolio.holdings.length) + " holdings to portfolio");

    // Simulate market price updates
    price_updates = {
        "AAPL": 180.25,
        "GOOGL": 2700.00,
        "MSFT": 290.00,
        "TSLA": 1100.00,
        "AMZN": 3250.00
    };

    update_market_prices(my_portfolio, price_updates);
    print("Updated market prices");

    // Generate analysis
    analysis = generate_portfolio_analysis(my_portfolio);
    diversification = calculate_diversification_score(my_portfolio);

    print("");
    print("Portfolio Analysis:");
    print("  Total holdings: " + to_string(analysis.total_holdings));
    print("  Portfolio value: $" + to_string(math_int(analysis.total_value)));
    print("  Total cost: $" + to_string(math_int(analysis.total_cost)));
    print("  Total gain/loss: $" + to_string(math_int(analysis.total_gain_loss)));
    print("  Return percentage: " + to_string(math_int(analysis.total_return_percentage)) + "%");
    print("  Winners: " + to_string(analysis.winners) + ", Losers: " + to_string(analysis.losers));
    print("  Largest holding: " + analysis.largest_holding.symbol + " ($" + to_string(math_int(analysis.largest_holding.value)) + ")");
    print("  Best performer: " + analysis.best_performer.symbol + " (+" + to_string(math_int(analysis.best_performer.percentage)) + "%)");
    print("  Worst performer: " + analysis.worst_performer.symbol + " (" + to_string(math_int(analysis.worst_performer.percentage)) + "%)");
    print("  Diversification score: " + to_string(diversification) + "/100");

    return {
        system: "portfolio_tracker",
        holdings_count: my_portfolio.holdings.length,
        portfolio_value: analysis.total_value,
        return_percentage: analysis.total_return_percentage,
        diversification_score: diversification
    };
}

// Main function to run all real-world application simulations
function main() {
    print("=============================================");
    print("  REAL-WORLD APPLICATIONS SIMULATION TEST");
    print("=============================================");

    results = {};

    results.ecommerce = ecommerce_order_processing();
    results.blog_cms = blog_content_management();
    results.task_management = task_management_system();
    results.portfolio_tracker = financial_portfolio_tracker();

    print("");
    print("=============================================");
    print("  ALL REAL-WORLD APPLICATION TESTS COMPLETED");
    print("=============================================");

    print("");
    print("Applications Summary:");
    print("  E-commerce System: Orders processed, validation working");
    print("  Blog CMS: " + to_string(results.blog_cms.posts_created) + " posts, " + to_string(results.blog_cms.total_views) + " total views");
    print("  Task Management: " + to_string(results.task_management.tasks_added) + " tasks, " + to_string(math_int(results.task_management.progress_percentage)) + "% progress");
    print("  Portfolio Tracker: " + to_string(results.portfolio_tracker.holdings_count) + " holdings, " + to_string(math_int(results.portfolio_tracker.return_percentage)) + "% return");

    return results;
}

// Execute comprehensive real-world applications simulation test
main();