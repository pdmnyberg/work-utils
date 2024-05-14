---
title: CRISPR Web App
---

# What is the project about?

- Making research data accessible
- "Genome wide CRISPR design tool"
- Initial code from a Jupyter notebook


# The challenges

- Limited budget
- Limited understanding of the scientific details
- Making sure we deliver the correct results
- Initially unknown deployment target


# Limited budget

- Split delivery into two parts
    - Initial simplified visualization
    - [Extended visualization using IGV](https://igv.org/web/release/2.15.5/examples/cram-vcf.html)
- Use safe and well known tools
- If it works, let it ship


# Limited understanding of the scientific details

- Keep an open dialog on unknowns
- Use internal resources (Agata) to help gain a better grasp of the concepts


# Making sure we deliver the correct results

- Write automatic tests that make sure the output remains the same
- Keep the Jupyter notebook comparable with the starting point


# Initially unknown deployment target

- Docker
- Hoping for the best
- https://serve.scilifelab.se/ (Deployment target)


# The technical choices

- Aim for a stateless backend
- Flask (A micro web framework using Python)
- Bootstrap (Basic styling and CSS)
- Mustache (Logic less tempaltes in JS)
- Flask-compress (Plugin to serve compressed HTTP results over Flask)
- Docker (Development and deployment using containers)


# The result

- Let's have a look at the current state
- Current state is the first part


# What could be done differently

- Use a client + backend approach
- Use React for client rendering
- Use a Rest API to serve search results
- Build the Excel and CSV on the client in order to split searches into smaller chunks
- Dump all the results from the Jupyter notebook into a database