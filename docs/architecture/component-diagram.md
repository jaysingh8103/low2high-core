# Component Diagram

```mermaid
graph TD
    UI[User Dashboard] --> API[Search Request API]
    API --> Discovery[Business Discovery Agent]
    Discovery --> Profile[Business Profile Agent]
    Profile --> Pipeline[Digital Analysis Pipeline]
    
    subgraph Pipeline
        Web[Website Agent]
        SEO[SEO Agent]
        Social[Social Agent]
    end
    
    Pipeline --> Comp[Competitor Analysis Agent]
    Comp --> Reco[Recommendation & ROI Agent]
    Reco --> Report[Report Generator]
```
